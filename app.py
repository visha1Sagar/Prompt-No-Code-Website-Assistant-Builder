from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from typing import List, Optional
import uuid
import json
from pyngrok import ngrok
import asyncio
from functools import lru_cache # For caching

import os

from starlette.middleware.cors import CORSMiddleware

from document_loader import process_documents_and_create_db, load_vector_database, query_vector_database, save_vector_database # Import save_vector_database
from new_web import main

from main import formulate_answer
from tree_from_json import extract_markdowns, create_tree_from_json
import requests
# --- FastAPI App ---
app = FastAPI()


origins = [
    "*",  # Allows all origins - for development. In production, specify your frontend domain(s).
    # "http://localhost",
    # "http://localhost:8080", # Example: if your frontend is on port 8080
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- In-memory cache for vector databases (bot_id -> vector_db) ---
# Using lru_cache for simple caching (you can adjust maxsize as needed)
@lru_cache(maxsize=128) # Example max size, adjust based on your needs
def cached_vector_database(bot_id: str):
    print(f"Cache miss for bot_id: {bot_id}. Loading from disk.")
    vector_db_path = os.path.join("vector_db_storage", bot_id) # Construct path
    db = load_vector_database(vector_db_path) # Load from disk using bot_id path
    return db

# --- Pydantic Models for Request Bodies ---
from pydantic import BaseModel

class CreateBotRequest(BaseModel):
    website_url: Optional[str] = None
    files: List[UploadFile] = File(default=[]) # Allow empty list of files

class QueryBotRequest(BaseModel):
    bot_id: str
    query: str
    context: str

# --- Helper function (Adapt process_configuration for FastAPI) ---
async def create_vector_db_from_config(website_url: Optional[str], files: List[UploadFile], bot_id: str): # Added bot_id
    """
    Processes website URL and documents to create a vector database and saves it to disk.
    Adapts the Gradio process_configuration logic for FastAPI.
    Returns the vector_db object or None if creation fails.
    """
    files_to_process = list(files or [])  # Handle None case for files

    if not website_url:
        return None

    print(f"Processing Website URL: {website_url}")
    try:
        import tempfile
        import os

        if not website_url.startswith(('http://', 'https://')):
            website_url = 'https://' + website_url

        await main(website_url, "crawl_json_temp.json")
        create_tree_from_json( "crawl_json_temp.json", "tree_output_temp.json")

        data = None
        with open("tree_output_temp.json", "r", encoding="utf-8") as file:
            data = json.load(file)
        markdown_text = extract_markdowns(data)

        # print("markdown : ", markdown_text)

        temp_file = tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False, encoding='utf-8')
        temp_file.write("\n\n".join(markdown_text))
        temp_file.flush()
        temp_file_path = temp_file.name
        print(f"Website content saved to temporary file: {temp_file_path}")
        files_to_process.append(temp_file)

    except requests.exceptions.RequestException as e:
        print(f"Error scraping website: {e}")
        return None # Website scraping failed, return None, handle error in endpoint
    except Exception as e:
        print(f"Unexpected error during website processing: {e}")
        return None # Unexpected error, return None, handle in endpoint


    if files_to_process:
        print("Processing documents and creating vector database...")
        vector_db_path = os.path.join("vector_db_storage", bot_id)
        vector_db = process_documents_and_create_db(files_to_process, persist_directory=vector_db_path)


        if vector_db: # Only save if vector_db was actually created
            vector_db_path = os.path.join("vector_db_storage", bot_id) # Path based on bot_id
            save_vector_database(vector_db, vector_db_path) # Save to disk with bot_id path
            print(f"Vector database saved to disk for bot_id: {bot_id} at: {vector_db_path}")
        else:
            print("Vector database creation failed, not saving to disk.")


        # Cleanup temp file after processing (if website was scraped)
        if website_url:
            temp_file.close()
            os.remove(temp_file.name)
            os.remove("tree_output_temp.json")
            os.remove("crawl_json_temp.json")
            print(f"Temporary website file cleaned up: {temp_file.name}")

        return vector_db # Return even if saving failed (creation might have succeeded)
    else:
        print("No website URL or documents provided.")
        return None



# --- Endpoint 1: Create Bot (`/create_bot`) ---
@app.post("/create_bot/")
async def create_bot_endpoint(
    website_url: str = Form(...), # Website URL is now a required Form parameter
    files: List[UploadFile] = File(default=[])): # File upload for documents (optional, allow empty list)

    """
    Endpoint to create a new chatbot bot (vector database) based on
    website URL and/or uploaded documents.
    """
    bot_id = str(uuid.uuid4()) # Generate unique bot ID
    vector_db = await create_vector_db_from_config(website_url, files, bot_id) # Pass bot_id

    if vector_db: # Creation might succeed even if saving fails, so check vector_db
        # No longer storing in bot_vector_dbs in memory directly.
        # Caching will happen in cached_vector_database function
        return {"bot_id": bot_id, "message": "Bot created and saved successfully!", "bot_id": bot_id}
    else:
        raise HTTPException(status_code=500, detail="Bot creation failed. Check server logs for errors.") # 500 for server-side issues


# --- Endpoint 2: Query Bot (`/query_bot`) ---
@app.post("/query_bot/")
async def query_bot_endpoint(request: QueryBotRequest):
    """
    Endpoint to query a specific chatbot bot by its ID.
    """
    bot_id = request.bot_id
    query = request.query

    context = request.context

    vector_db = cached_vector_database(bot_id) # Load from cache or disk via cache function
    if not vector_db:
        raise HTTPException(status_code=404, detail=f"Bot with id '{bot_id}' not found or could not be loaded.") # Updated message

    response = query_vector_database(vector_db, context+"\n"+query) # Query vector DB
    if response:
        answer = formulate_answer(query, response, context) # Formulate answer using LLM
        return {"answer": answer}
    else:
        return {"answer": "No relevant information found in the bot's documents for your query."}


if __name__ == "__main__":
    import uvicorn

    # Ensure vector_db_storage directory exists
    if not os.path.exists("vector_db_storage"):
        os.makedirs("vector_db_storage")

    ngrok_tunnel = ngrok.connect(8000)
    public_url = ngrok_tunnel.public_url
    print(f"Public ngrok URL: {public_url}")  # Output public URL - important!

    uvicorn.run(app, host="localhost", port=8000)