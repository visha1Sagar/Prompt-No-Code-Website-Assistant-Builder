import os
from typing import List
import dotenv
dotenv.load_dotenv('.env')
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader, TextLoader

# --- Configuration ---
VECTOR_DB_PATH = "faiss_index"  # Path to save/load FAISS index
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def load_document(file_path: str):
    """Loads document based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        print(f"Loading PDF: {file_path}")
        loader = PyPDFLoader(file_path)
    elif ext == '.txt':
        print(f"Loading TXT: {file_path}")
        loader = TextLoader(file_path)
    else:
        raise ValueError(f"Unsupported document type: {ext}")
    return loader.load()

def chunk_documents(documents: List):
    """Splits documents into text chunks."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    chunks = text_splitter.split_documents(documents)
    return chunks


def create_vector_database_from_documents(chunks):
    """Creates and saves a FAISS vector database from text chunks."""
    embeddings = OpenAIEmbeddings()
    vector_db = FAISS.from_documents(chunks, embeddings)
    save_vector_database(vector_db)
    return vector_db

def save_vector_database(vector_db):
    """Saves FAISS vector database to disk."""
    vector_db.save_local(VECTOR_DB_PATH)
    print(f"Vector database saved to: {VECTOR_DB_PATH}")

def load_vector_database():
    embeddings = OpenAIEmbeddings()
    if os.path.exists(f"{VECTOR_DB_PATH}/index.faiss") and os.path.exists(f"{VECTOR_DB_PATH}/index.pkl"): # Using VECTOR_DB_PATH here
        vector_db = FAISS.load_local(VECTOR_DB_PATH, embeddings, allow_dangerous_deserialization=True)
        print(f"Vector database loaded from: {VECTOR_DB_PATH}")
        return vector_db
    else:
        print("No existing vector database found. Please create one first.")
        return None

def process_documents_and_create_db(files: List):
    """
    Processes uploaded document files: loads, chunks, and creates a FAISS vector database.
    """
    if not files:
        print("No files uploaded for processing.")
        return None

    all_documents = []
    for file in files:
        try:
            documents = load_document(file.name) # Gradio File object has 'name' as path
            all_documents.extend(documents)
        except ValueError as e:
            print(f"Skipping file {file.name}: {e}") # Log unsupported file types, continue processing others
        except Exception as e:
            print(f"Error loading file {file.name}: {e}") # Log other errors, continue

    if not all_documents:
        print("No valid documents loaded for vector database creation.")
        return None

    print(f"Loaded {len(all_documents)} documents.")
    text_chunks = chunk_documents(all_documents)
    print(f"Created {len(text_chunks)} text chunks.")
    vector_db = create_vector_database_from_documents(text_chunks) # Creates and saves DB
    return vector_db


def query_vector_database(vector_db, query, num_results=4):  # Added num_results parameter
    """Queries the FAISS vector database and returns relevant document chunks."""
    if not vector_db:
        print("Error: Vector database not loaded for querying.")
        return None

    embeddings = OpenAIEmbeddings()  # Initialize embeddings again (ensure API key is set)
    query_vector = embeddings.embed_query(query)  # Embed the user query
    # Perform similarity search in FAISS vector database
    search_results_with_scores = vector_db.similarity_search_with_score_by_vector(
        query_vector, k=num_results  # k is the number of nearest neighbors to retrieve
    )
    # Extract documents from results (and optionally scores if needed)
    relevant_documents = [doc for doc, score in search_results_with_scores]  # Just get documents for now
    return relevant_documents


# --- Example Usage (for testing in document_handler.py directly) ---
if __name__ == "__main__":

    test_files = ["dummy.txt", "dummy_pdf.pdf"]
    print("--- Processing Documents and Creating Vector DB ---")
    vector_db = process_documents_and_create_db([open(f, 'rb') for f in test_files])
    if vector_db:
        print("\n--- Vector DB Created Successfully! ---")
        loaded_db = load_vector_database()  # Test loading
        if loaded_db:
            print("\n--- Vector DB Loaded Successfully from Disk! ---")
        else:
            print("\n--- Error loading Vector DB ---")
    else:
        print("\n--- Vector DB Creation Failed ---")