import os
import tempfile
from typing import List, Optional
import dotenv
from fastapi import UploadFile
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter

dotenv.load_dotenv('.env')
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Ensure OpenAI API key is loaded from environment
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please add your OpenAI API key to the .env file.")
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_experimental.text_splitter import SemanticChunker
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def load_document(file_path: str) -> List[Document]:
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
        logger.error(f"Error loading document {file_path}: {e}")
        return []
    return loader.load()

def chunk_documents(documents: List[Document], strategy: str = "recursive") -> List[Document]:
    """Enhanced chunking with multiple strategies"""
    # Use recursive chunking by default instead of semantic to avoid OpenAI dependency
    chunkers = {
        "recursive": RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\n\n", "\n", ". ", "! ", "? ", " ", ""]
        ),
        "markdown": MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header 1"),
                ("##", "Header 2"),
                ("###", "Header 3")
            ]
        )
    }

    all_chunks = []
    for doc in documents:
        try:
            if strategy == "auto":
                content_type = doc.metadata.get('content_type', 'text')
                chunker = chunkers["markdown" if content_type == "markdown" else "recursive"]
            else:
                chunker = chunkers[strategy]

            chunks = chunker.split_documents([doc])
            for chunk in chunks:
                chunk.metadata.update({
                    'document_id': hash(doc.page_content),
                    'chunk_strategy': strategy
                })
            all_chunks.extend(chunks)

        except Exception as e:
            logger.warning(f"Chunking failed for document {doc.metadata.get('source')}: {str(e)}")
            continue

    return all_chunks

def create_vector_database_from_documents(chunks, persist_directory) -> Chroma:
    """Creates and saves a Chroma vector database from text chunks."""
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
    return vector_db

def save_vector_database(vector_db, persist_directory):
    """Saves Chroma vector database to disk to a specific directory."""
    logger.info(f"Attempting to persist vector database of type: {type(vector_db)}")
    try:
        vector_db.persist()
        logger.info(f"Vector database saved to: {persist_directory}")
    except Exception as e:
        logger.error(f"Error during vector_db.persist(): {e}")
        raise

def load_vector_database(persist_directory) -> Optional[Chroma]:
    """Loads Chroma vector database from disk from a specific directory."""
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    try:
        vector_db = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
        logger.info(f"Vector database loaded from: {persist_directory}")
        return vector_db
    except Exception as e:
        logger.error(f"Error loading vector database from {persist_directory}: {e}")
        return None

def process_documents_and_create_db(files, persist_directory=None, chunk_strategy: str = "recursive") -> Optional[Chroma]:
    """Processes document files, chunks them, and creates/saves a vector database."""
    documents = []
    if not files:
        logger.info("No files provided for processing.")
        return None

    for file in files:
        file_name = None
        file_path_to_load = None

        if isinstance(file, UploadFile):
            file_name = file.filename
            file_path_to_load = file.file
            logger.debug(f"Detected UploadFile: {file_name}")
        elif hasattr(file, 'filename'):
            file_name = file.filename
            file_path_to_load = file.file.name if hasattr(file, 'file') and hasattr(file.file, 'name') else file.name
            logger.debug(f"Detected file-like object with filename: {file_name}")
        elif isinstance(file, tempfile._TemporaryFileWrapper):
            file_name = file.name
            file_path_to_load = file.name
            logger.debug(f"Detected tempfile: {file_name}")
        elif isinstance(file, str):
            file_name = file
            file_path_to_load = file
            logger.debug(f"Detected file path string: {file_name}")
        elif isinstance(file, bytes):
            file_name = "in_memory_data.txt"
            file_path_to_load = tempfile.NamedTemporaryFile(mode='wb+', suffix=".txt", delete=False)
            file_path_to_load.write(file)
            file_path_to_load.flush()
            file_path_to_load = file_path_to_load.name
            logger.debug(f"Detected raw bytes data, saved to temp file: {file_path_to_load}")
        else:
            file_name = "unknown_file"
            file_path_to_load = None
            logger.warning(f"Unknown file type encountered: {type(file)}, skipping.")

        logger.info(f"Loading document: {file_name}, Type: {type(file)}")

        try:
            if file_path_to_load:
                loaded_docs = load_document(file_path_to_load)
                documents.extend(loaded_docs)
            else:
                logger.warning(f"Skipping file as no path to load: {file_name}")
                continue
        except Exception as e:
            logger.error(f"Error loading file {file_name}: {e}")
            continue

    if not documents:
        logger.info("No documents loaded successfully from the provided files.")
        return None

    chunks = chunk_documents(documents, strategy=chunk_strategy)
    vector_db = create_vector_database_from_documents(chunks, persist_directory)
    return vector_db

def query_vector_database(vector_db, query, num_results=4) -> List[Document]:
    """Queries the Chroma vector database and returns relevant document chunks."""
    if not vector_db:
        logger.error("Error: Vector database not loaded for querying.")
        return []

    relevant_documents = vector_db.similarity_search(query, k=num_results)
    return relevant_documents