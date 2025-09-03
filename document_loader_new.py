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
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_experimental.text_splitter import SemanticChunker
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_embeddings_function():
    """Initialize embeddings function using Sentence Transformers only."""
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    except ImportError:
        logger.error("HuggingFace embeddings not available. Please install sentence-transformers")
        raise RuntimeError("No embedding function available. Please install sentence-transformers")

def load_document(file_path: str) -> List[Document]:
    """Loads document based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    try:
        if ext == '.pdf':
            print(f"Loading PDF: {file_path}")
            loader = PyPDFLoader(file_path)
        elif ext == '.txt':
            print(f"Loading TXT: {file_path}")
            loader = TextLoader(file_path, encoding='utf-8')
        else:
            logger.warning(f"Unsupported file extension: {ext}")
            return []
        
        documents = loader.load()
        logger.info(f"Loaded {len(documents)} documents from {file_path}")
        return documents
    except Exception as e:
        logger.error(f"Error loading {file_path}: {str(e)}")
        return []

def chunk_documents(documents: List[Document], strategy: str = "semantic") -> List[Document]:
    """Enhanced chunking with multiple strategies using only Sentence Transformers"""
    
    # Always use HuggingFace embeddings for semantic chunking
    try:
        chunkers = {
            "semantic": SemanticChunker(get_embeddings_function()),
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

        # Use the requested strategy, fallback to recursive if semantic fails
        if strategy in chunkers and chunkers[strategy] is not None:
            try:
                if strategy == "markdown":
                    # Markdown chunking first, then recursive for smaller chunks
                    md_chunks = chunkers["markdown"].split_documents(documents)
                    final_chunks = chunkers["recursive"].split_documents(md_chunks)
                    return final_chunks
                else:
                    chunks = chunkers[strategy].split_documents(documents)
                    return chunks
            except Exception as e:
                logger.warning(f"Error with {strategy} chunking: {e}. Falling back to recursive.")
                chunks = chunkers["recursive"].split_documents(documents)
                return chunks
        else:
            logger.warning(f"Strategy {strategy} not available. Using recursive.")
            chunks = chunkers["recursive"].split_documents(documents)
            return chunks
    
    except Exception as e:
        logger.error(f"Error in chunking: {e}")
        # Final fallback - simple recursive chunking
        fallback_chunker = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        return fallback_chunker.split_documents(documents)

def augment_chunk_metadata(chunks: List[Document]) -> List[Document]:
    """Add enhanced metadata to chunks."""
    augmented = []
    for i, chunk in enumerate(chunks):
        # Enhance metadata
        chunk.metadata.update({
            'chunk_id': i,
            'word_count': len(chunk.page_content.split()),
            'char_count': len(chunk.page_content)
        })
        augmented.append(chunk)
    return augmented

def filter_chunks(chunks: List[Document], min_words: int = 10) -> List[Document]:
    """Filter out chunks that are too small or contain mostly whitespace."""
    filtered = []
    for chunk in chunks:
        word_count = len(chunk.page_content.strip().split())
        if word_count >= min_words and chunk.page_content.strip():
            filtered.append(chunk)
    
    logger.info(f"Filtered {len(chunks)} chunks down to {len(filtered)} meaningful chunks")
    return filtered

def deduplicate_chunks(chunks: List[Document], similarity_threshold: float = 0.9) -> List[Document]:
    """Remove near-duplicate chunks based on content similarity."""
    if not chunks:
        return chunks
    
    unique_chunks = [chunks[0]]  # Keep the first chunk
    
    for chunk in chunks[1:]:
        is_duplicate = False
        for unique_chunk in unique_chunks:
            # Simple similarity check based on common words
            words1 = set(chunk.page_content.lower().split())
            words2 = set(unique_chunk.page_content.lower().split())
            
            if words1 and words2:
                overlap = len(words1.intersection(words2))
                union = len(words1.union(words2))
                similarity = overlap / union if union > 0 else 0
                
                if similarity > similarity_threshold:
                    is_duplicate = True
                    break
        
        if not is_duplicate:
            unique_chunks.append(chunk)
    
    logger.info(f"Deduplicated {len(chunks)} chunks down to {len(unique_chunks)} unique chunks")
    return unique_chunks

def load_vector_database(persist_directory) -> Optional[Chroma]:
    """Load an existing vector database from disk."""
    try:
        vector_db = Chroma(
            persist_directory=persist_directory,
            embedding_function=get_embeddings_function()
        )
        logger.info(f"Vector database loaded from: {persist_directory}")
        return vector_db
    except Exception as e:
        logger.error(f"Error loading vector database: {e}")
        return None

def process_documents_and_create_db(files, persist_directory=None, chunk_strategy: str = "semantic") -> Optional[Chroma]:
    """Process documents and create a vector database."""
    
    all_documents = []
    
    for file in files:
        logger.info(f"Loading document: {file}, Type: {type(file)}")
        
        # Handle different file types
        try:
            if isinstance(file, UploadFile):
                # Handle FastAPI UploadFile
                file_extension = os.path.splitext(file.filename)[1].lower()
                
                with tempfile.NamedTemporaryFile(mode='wb+', suffix=file_extension, delete=False) as temp_file:
                    content = file.file.read()
                    temp_file.write(content)
                    temp_file.flush()
                    file_path_to_load = temp_file.name
                    
            elif isinstance(file, tempfile._TemporaryFileWrapper):
                # Handle temporary file wrapper
                file_path_to_load = file.name
                
            elif isinstance(file, str):
                # Handle file path string
                file_path_to_load = file
                
            else:
                # Handle file-like object
                file_path_to_load = tempfile.NamedTemporaryFile(mode='wb+', suffix=".txt", delete=False)
                content = file.read()
                file_path_to_load.write(content.encode() if isinstance(content, str) else content)
                file_path_to_load.flush()
                file_path_to_load = file_path_to_load.name
                
            documents = load_document(file_path_to_load)
            all_documents.extend(documents)
            
        except Exception as e:
            logger.error(f"Error processing file {file}: {e}")
            continue
    
    if not all_documents:
        logger.warning("No documents were successfully loaded")
        return None
    
    # Process documents
    chunks = chunk_documents(all_documents, strategy=chunk_strategy)
    
    # Apply filtering and processing
    chunks = filter_chunks(chunks)
    chunks = deduplicate_chunks(chunks)
    chunks = augment_chunk_metadata(chunks)
    
    # Add chunk strategy to metadata
    for chunk in chunks:
        chunk.metadata['chunk_strategy'] = chunk_strategy
    
    logger.info(f"Total chunks created: {len(chunks)}")
    
    # Create vector database
    try:
        vector_db = Chroma.from_documents(
            documents=chunks,
            embedding=get_embeddings_function(),
            persist_directory=persist_directory
        )
        logger.info(f"Vector database created with {len(chunks)} chunks")
        return vector_db
    except Exception as e:
        logger.error(f"Error creating vector database: {e}")
        return None

def query_vector_database(vector_db, query, num_results=4) -> List[Document]:
    """Query the vector database and return similar documents."""
    try:
        results = vector_db.similarity_search(query, k=num_results)
        return results
    except Exception as e:
        logger.error(f"Error querying vector database: {e}")
        return []
