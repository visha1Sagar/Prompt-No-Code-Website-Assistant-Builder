import tempfile

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
import uuid
import json
import os

from langchain_chroma import Chroma
from pydantic import BaseModel

from starlette.middleware.cors import CORSMiddleware
from functools import lru_cache
import logging

from document_loader import process_documents_and_create_db, load_vector_database, query_vector_database
from main_gradio import formulate_answer
from crawler.main_crawler import call_crawler
from text_postprocessing.remove_header import remove_header_footer
from text_postprocessing.tree_from_json import extract_markdowns, create_tree_from_json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@lru_cache(maxsize=128)
def cached_vector_database(bot_id: str) -> Optional[Chroma]:
    logger.info(f"Cache miss for bot_id: {bot_id}. Loading from disk.")
    vector_db_path = os.path.join("vector_db_storage", bot_id)
    db = load_vector_database(vector_db_path)
    return db

class CreateBotRequest(BaseModel):
    website_url: Optional[str] = None
    files: List[UploadFile] = File(default=[])

class QueryBotRequest(BaseModel):
    bot_id: str
    query: str
    context: str

async def create_vector_db_from_config(website_url: Optional[str], files: List[UploadFile], bot_id: str) -> Optional[Chroma]:
    files_to_process = list(files or [])

    if website_url:
        logger.info(f"Processing Website URL: {website_url}")
        try:
            if not website_url.startswith(('http://', 'https://')):
                website_url = 'https://' + website_url

            # Call crawler to crawl the website
            await call_crawler(website_url, "crawl_json_temp.json")
            
            # Post-process the crawled data
            new_file = remove_header_footer("crawl_json_temp.json")
            create_tree_from_json("crawl_json_temp.json", "tree_output_temp.json")
            
            # Extract markdown content from the processed data
            markdowns = extract_markdowns("tree_output_temp.json")
            
            # Add the extracted markdowns to files to process
            if markdowns:
                # Create temporary files from the markdowns
                for i, markdown in enumerate(markdowns):
                    temp_file = f"website_content_{i}.md"
                    with open(temp_file, 'w', encoding='utf-8') as f:
                        f.write(markdown)
                    files_to_process.append(temp_file)
                logger.info(f"Added {len(markdowns)} markdown files from website crawling")

        except Exception as e:
            logger.error(f"Error during website processing: {e}")
            # Don't return None, continue with file processing if available

    if files_to_process:
        logger.info("Processing documents and creating vector database...")
        vector_db_path = os.path.join("vector_db_storage", bot_id)
        vector_db = process_documents_and_create_db(files_to_process, persist_directory=vector_db_path)

        if vector_db:
            logger.info(f"Vector database saved to disk for bot_id: {bot_id} at: {vector_db_path}")
        else:
            logger.warning("Vector database creation failed, not saving to disk.")

        # Clean up temporary files
        import glob
        temp_files = glob.glob("crawl_json_temp.json") + glob.glob("tree_output_temp.json") + glob.glob("website_content_*.md")
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except FileNotFoundError:
                pass

        return vector_db
    else:
        logger.warning("No website URL processing available and no files provided.")
        # For now, create a basic vector DB even without content
        # This allows the bot to be created even if crawling is disabled
        vector_db_path = os.path.join("vector_db_storage", bot_id)
        
        # Create empty temp file as placeholder
        temp_file = tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False, encoding='utf-8')
        temp_file.write("Bot created successfully. Website crawling is currently disabled.")
        temp_file.flush()
        temp_file.close()
        
        vector_db = process_documents_and_create_db([temp_file.name], persist_directory=vector_db_path)
        os.remove(temp_file.name)
        
        return vector_db

@app.post("/create_bot/")
async def create_bot_endpoint(
    website_url: str = Form(...),
    files: List[UploadFile] = File(default=[])):

    bot_id = str(uuid.uuid4())
    vector_db = await create_vector_db_from_config(website_url, files, bot_id)

    if vector_db:
        return {"bot_id": bot_id, "message": "Bot created and saved successfully!"}
    else:
        raise HTTPException(status_code=500, detail="Bot creation failed. Check server logs for errors.")

@app.post("/query_bot/")
async def query_bot_endpoint(request: QueryBotRequest):
    bot_id = request.bot_id
    query = request.query
    context = request.context

    vector_db = cached_vector_database(bot_id)
    if not vector_db:
        raise HTTPException(status_code=404, detail=f"Bot with id '{bot_id}' not found or could not be loaded.")

    response = query_vector_database(vector_db, context + "\n" + query)

    if response:
        answer = formulate_answer(query, response, context)
        return {"answer": answer}
    else:
        return {"answer": "No relevant information found in the bot's documents for your query."}

if __name__ == "__main__":
    import uvicorn

    # Ensure vector_db_storage directory exists
    if not os.path.exists("vector_db_storage"):
        os.makedirs("vector_db_storage")



    uvicorn.run(app, host="localhost", port=8000)