import asyncio
import tempfile

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import List, Optional
import uuid
import json
import os

from langchain_chroma import Chroma
from pydantic import BaseModel

from starlette.middleware.cors import CORSMiddleware
from cachetools import LRUCache
import logging
import sys

import asyncio

from document_loader import process_documents_and_create_db, load_vector_database, query_vector_database
from main_gradio import formulate_answer
from crawler.main_crawler import call_crawler
from text_postprocessing.remove_header import remove_header_footer
from text_postprocessing.tree_from_json import extract_markdowns, create_tree_from_json
from user_api_storage import api_key_storage

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": f"Validation error: {exc.errors()}"}
    )

# CORS configuration for Vercel frontend
origins = [
    "http://localhost:3000",  # Local development
    "https://*.vercel.app",   # Vercel deployments
    # Add your specific Vercel URL here:
    # "https://your-app-name.vercel.app",
]

# Allow all origins for development, but restrict in production
if os.getenv("ENVIRONMENT") == "development":
    origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

def get_size(obj):
    # A helper function to get the size of an object in memory
    # This is a simplified example; for complex objects, you might need a more sophisticated approach
    return sys.getsizeof(obj)

# Using cachetools.LRUCache for more memory-efficient caching
# This cache will hold up to 100MB of vector databases.
vector_db_cache = LRUCache(maxsize=100 * 1024 * 1024, getsizeof=get_size)

def cached_vector_database(bot_id: str) -> Optional[Chroma]:
    if bot_id in vector_db_cache:
        logger.info(f"Cache hit for bot_id: {bot_id}.")
        return vector_db_cache[bot_id]
    
    logger.info(f"Cache miss for bot_id: {bot_id}. Loading from disk.")
    vector_db_path = os.path.join("vector_db_storage", bot_id)
    
    # The load_vector_database function will try different embeddings automatically
    db = load_vector_database(vector_db_path)
    
    if db:
        vector_db_cache[bot_id] = db
    return db

class CreateBotRequest(BaseModel):
    website_url: Optional[str] = None
    files: List[UploadFile] = File(default=[])

class QueryBotRequest(BaseModel):
    bot_id: str
    query: str
    context: str
    user_id: Optional[str] = None  # User ID to look up stored API key
    model: Optional[dict] = None  # {provider: str, model_name: str, api_key: str}

class StoreAPIKeyRequest(BaseModel):
    user_id: str
    provider: str
    api_key: str
    model_name: Optional[str] = None

class DeleteAPIKeyRequest(BaseModel):
    user_id: str
    provider: str

async def create_vector_db_from_config(
    website_url: Optional[str], 
    files: List[UploadFile], 
    bot_id: str,
    model_provider: str,
    api_key: str
) -> Optional[Chroma]:
    files_to_process = list(files or [])
    temp_files_to_clean = []

    if website_url:
        logger.info(f"Processing Website URL: {website_url}")
        try:
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as crawl_json_temp:
                crawl_json_path = crawl_json_temp.name
            
            await call_crawler(website_url, crawl_json_path)
            
            new_file_content = remove_header_footer(crawl_json_path)

            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix=".json") as tree_output_temp:
                tree_output_path = tree_output_temp.name

            create_tree_from_json(crawl_json_path, tree_output_path)

            with open(tree_output_path, "r", encoding="utf-8") as file:
                data = json.load(file)
            markdown_text = extract_markdowns(data)

            if not markdown_text:
                logger.warning("No markdown content extracted from website")
                markdown_text = ["No content could be extracted from the website."]

            with tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False, encoding='utf-8') as temp_markdown_file:
                temp_markdown_file.write("\n\n".join(markdown_text))
                temp_markdown_file.flush()
                files_to_process.append(temp_markdown_file.name)
                temp_files_to_clean.append(temp_markdown_file.name)

            os.remove(crawl_json_path)
            os.remove(tree_output_path)

        except Exception as e:
            logger.error(f"Error during website processing: {e}")
            for temp_file_path in temp_files_to_clean:
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
            return None

    if files_to_process:
        vector_db_path = os.path.join("vector_db_storage", bot_id)
        
        processed_files = []
        for file in files_to_process:
            if isinstance(file, str):
                processed_files.append(file)
            elif isinstance(file, UploadFile):
                with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as temp_upload:
                    temp_upload.write(await file.read())
                    processed_files.append(temp_upload.name)
                    temp_files_to_clean.append(temp_upload.name)
        
        loop = asyncio.get_running_loop()
        vector_db = await loop.run_in_executor(
            None,
            lambda: process_documents_and_create_db(
                processed_files,
                vector_db_path,
                model_provider,
                api_key
            )
        )

        if vector_db:
            logger.info(f"Vector database saved to disk for bot_id: {bot_id} at: {vector_db_path}")
        else:
            logger.warning("Vector database creation failed, not saving to disk.")

        for temp_file_path in temp_files_to_clean:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                logger.info(f"Temporary file cleaned up: {temp_file_path}")

        return vector_db
    else:
        logger.warning("No website URL or documents provided.")
        return None

@app.post("/create_bot/")
async def create_bot_endpoint(
    website_url: Optional[str] = Form(None),
    files: List[UploadFile] = File(default=[]),
    model_provider: Optional[str] = Form(None),
    api_key: Optional[str] = Form(None),
    user_id: Optional[str] = Form(None)
):
    logger.info(f"Received create_bot request: website_url={website_url}, files_count={len(files)}, user_id={user_id}")
    logger.info("Note: Embeddings will use environment OpenAI API key, user API keys are for QnA only")
    
    # Validate that at least one of website_url or files is provided
    if not website_url and not files:
        raise HTTPException(
            status_code=422, 
            detail="Either website_url or files must be provided"
        )
    
    bot_id = str(uuid.uuid4())
    vector_db = await create_vector_db_from_config(
        website_url, files, bot_id, None, None  # No need to pass user API keys for embeddings
    )

    if vector_db:
        return {"bot_id": bot_id, "message": "Bot created and saved successfully!"}
    else:
        raise HTTPException(status_code=500, detail="Bot creation failed. Check server logs for errors.")

@app.post("/query_bot/")
async def query_bot_endpoint(request: QueryBotRequest):
    bot_id = request.bot_id
    query = request.query
    context = request.context
    user_id = request.user_id
    model_info = request.model

    vector_db = cached_vector_database(bot_id)
    if not vector_db:
        raise HTTPException(status_code=404, detail=f"Bot with id '{bot_id}' not found or could not be loaded.")

    response = query_vector_database(vector_db, context + "\n" + query)

    if response:
        # Try to get user's stored API key for QnA
        final_model_info = model_info
        if user_id and not model_info:
            # Look up user's primary model
            user_models = api_key_storage.get_user_models(user_id)
            if user_models:
                # For now, try to find an OpenAI model
                openai_model = user_models.get('openai')
                if openai_model:
                    final_model_info = {
                        'provider': 'openai',
                        'model_name': openai_model.get('model_name', 'gpt-4o-mini'),
                        'api_key': openai_model['api_key']
                    }
                    logger.info(f"Using stored API key for QnA for user {user_id}")
        
        answer = formulate_answer(query, response, context, final_model_info)
        return {"answer": answer}
    else:
        return {"answer": "No relevant information found in the bot's documents for your query."}

@app.post("/store_api_key/")
async def store_api_key_endpoint(request: StoreAPIKeyRequest):
    """Store API key for a user and provider."""
    success = api_key_storage.store_api_key(
        request.user_id, 
        request.provider, 
        request.api_key, 
        request.model_name
    )
    if success:
        return {"message": "API key stored successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to store API key")

@app.get("/get_user_models/{user_id}")
async def get_user_models_endpoint(user_id: str):
    """Get all AI models for a user."""
    models = api_key_storage.get_user_models(user_id)
    return {"models": models}

@app.delete("/delete_api_key/")
async def delete_api_key_endpoint(request: DeleteAPIKeyRequest):
    """Delete API key for a user and provider."""
    success = api_key_storage.delete_api_key(request.user_id, request.provider)
    if success:
        return {"message": "API key deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="API key not found")

@app.get("/health")
async def health_check():
    """Health check endpoint for Docker health checks"""
    return {"status": "healthy", "message": "Service is running"}

if __name__ == "__main__":
    import uvicorn

    # Ensure vector_db_storage directory exists
    if not os.path.exists("vector_db_storage"):
        os.makedirs("vector_db_storage")



    uvicorn.run(app, host="localhost", port=8000)