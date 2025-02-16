import os
import tempfile
from typing import List
import dotenv
from fastapi import UploadFile

dotenv.load_dotenv('.env')
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# --- Configuration ---
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_document(file_path: str):
    """Loads document based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            print(f"Loading PDF: {file_path}")
            loader = PyPDFLoader(file_path)
        elif ext == '.txt':
            print(f"Loading TXT: {file_path}")
            loader = TextLoader(file_path, encoding="utf8")
        else:
            raise ValueError(f"Unsupported document type: {ext}")

    except Exception as e:
        print(e)
    return loader.load()

def chunk_documents(documents: List):
    """Splits documents into text chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vector_database_from_documents(chunks, persist_directory): # Added persist_directory
    """Creates and saves a FAISS vector database from text chunks."""
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(chunks, embeddings)
    save_vector_database(vector_db, persist_directory) # Use save_vector_database with directory
    return vector_db

def save_vector_database(vector_db, persist_directory): # Added persist_directory
    """Saves FAISS vector database to disk to a specific directory."""
    if not os.path.exists(persist_directory): # Create directory if it doesn't exist
        os.makedirs(persist_directory)
    vector_db.save_local(persist_directory)
    print(f"Vector database saved to: {persist_directory}")

def load_vector_database(persist_directory): # Added persist_directory
    embeddings = OpenAIEmbeddings()
    index_path = os.path.join(persist_directory, "index.faiss") # Construct path
    pkl_path = os.path.join(persist_directory, "index.pkl") # Construct path

    if os.path.exists(index_path) and os.path.exists(pkl_path):
        try:
            vector_db = FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)
            print(f"Vector database loaded from: {persist_directory}")
            return vector_db
        except Exception as e:
            print(f"Error loading vector database from {persist_directory}: {e}")
            return None # Handle loading errors gracefully
    else:
        print(f"No existing vector database found at: {persist_directory}")
        return None

def process_documents_and_create_db(files, persist_directory=None):
    """Processes document files, chunks them, and creates/saves a vector database."""
    documents = []
    if not files:
        print("No files provided for processing.")
        return None

    for file in files:
        file_name = None
        file_path_to_load = None

        # --- Robustly determine file_name and file_path ---
        if isinstance(file, UploadFile): # Check for FastAPI UploadFile first
            file_name = file.filename
            # For UploadFile, we need to use file.file to access the SpooledTemporaryFile
            file_path_to_load = file.file  # Pass the SpooledTemporaryFile object itself
            print(f"Detected UploadFile: {file_name}") # Debug log for UploadFile
        elif hasattr(file, 'filename'): # Check for other file-like objects with 'filename' (e.g., tempfile)
            file_name = file.filename
            file_path_to_load = file.file.name if hasattr(file, 'file') and hasattr(file.file, 'name') else file.name # Handle different nested attrs
            print(f"Detected file-like object with filename: {file_name}") # Debug
        elif isinstance(file, tempfile._TemporaryFileWrapper): # Explicit tempfile check (might be redundant)
            file_name = file.name
            file_path_to_load = file.name
            print(f"Detected tempfile: {file_name}") # Debug
        elif isinstance(file, str): # Assume it's a file path string
            file_name = file # Use file path as name for logging
            file_path_to_load = file
            print(f"Detected file path string: {file_name}") # Debug
        elif isinstance(file, bytes): # Handle raw bytes input (e.g., from memory) - optional, might not be needed
            file_name = "in_memory_data.txt" # Or generate a unique name
            file_path_to_load = tempfile.NamedTemporaryFile(mode='wb+', suffix=".txt", delete=False)
            file_path_to_load.write(file) # Write bytes to temp file
            file_path_to_load.flush() # Ensure data is written
            file_path_to_load = file_path_to_load.name # Get temp file path after writing
            print(f"Detected raw bytes data, saved to temp file: {file_path_to_load}") # Debug

        else:
            file_name = "unknown_file"
            file_path_to_load = None
            print(f"Unknown file type encountered: {type(file)}, skipping.") # More informative skip log


        print(f"Loading document: {file_name}, Type: {type(file)}")

        try:
            if file_path_to_load:
                loaded_docs = load_document(file_path_to_load) # Pass file_path_to_load (could be path string or file-like obj)
                documents.extend(loaded_docs)
            else:
                print(f"Skipping file as no path to load: {file_name}")
                continue # Skip to next file


        except UnicodeDecodeError as e:
            file_name_for_error = file_name if file_name else "unknown_file" # Use file_name if available
            print(f"UnicodeDecodeError loading file {file_name_for_error}: {e}")
            print(f"Trying to load {file_name_for_error} with utf-8 encoding explicitly...")
            try:
                loader = TextLoader(file_path_to_load, encoding="utf-8") # Use file_path_to_load
                loaded_docs = loader.load()
                documents.extend(loaded_docs)
                print(f"Successfully loaded {file_name_for_error} with utf-8 encoding after retry.")
            except Exception as retry_e:
                file_name_for_retry_error = file_name if file_name else "unknown_file"
                print(f"Failed to load {file_name_for_retry_error} even with explicit utf-8 encoding: {retry_e}")
                print(f"Skipping file: {file_name_for_retry_error} due to encoding issues.")
                continue # Skip on retry error
        except Exception as e:
            file_name_for_general_error = file_name if file_name else "unknown_file"
            print(f"Error loading file {file_name_for_general_error}: {e}")
            continue # Skip on general error


    if not documents:
        print("No documents loaded successfully from the provided files.")
        return None

    chunks = chunk_documents(documents)
    vector_db = create_vector_database_from_documents(chunks, persist_directory) # Pass persist_directory
    # save_vector_database(vector_db, persist_directory) # Already saved inside create_vector_database_from_documents
    return vector_db



def query_vector_database(vector_db, query, num_results=4):
    """Queries the FAISS vector database and returns relevant document chunks."""
    if not vector_db:
        print("Error: Vector database not loaded for querying.")
        return None

    embeddings = OpenAIEmbeddings()
    query_vector = embeddings.embed_query(query)
    search_results_with_scores = vector_db.similarity_search_with_score_by_vector(
        query_vector, k=num_results
    )
    relevant_documents = [doc for doc, score in search_results_with_scores]
    return relevant_documents


# --- Example Usage (for testing in document_handler.py directly) ---
if __name__ == "__main__":

    # ... rest of the test code ...
    bot_id_for_test = "test_bot_id_123" # Example bot_id for testing
    test_files = ["dummy.txt", "dummy_pdf.pdf"]
    persist_dir_test = os.path.join("vector_db_storage", bot_id_for_test) # Path for this test bot

    # test_files = ["dummy.txt", "dummy_pdf.pdf"]
    print("--- Processing Documents and Creating Vector DB ---")
    vector_db = process_documents_and_create_db([open(f, 'rb') for f in test_files], persist_dir_test)


    # print("--- Processing Documents and Creating Vector DB ---")
    # vector_db =
    # ([open(f, 'rb') for f in test_files], persist_dir_test) # Pass persist dir
    if vector_db:
        print("\n--- Vector DB Created and Saved Successfully! ---")
        loaded_db = load_vector_database(persist_dir_test)  # Test loading, pass persist dir
        if loaded_db:
            print(f"\n--- Vector DB Loaded Successfully from Disk from: {persist_dir_test}! ---")
        else:
            print("\n--- Error loading Vector DB ---")
    else:
        print("\n--- Vector DB Creation Failed ---")