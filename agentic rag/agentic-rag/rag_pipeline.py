from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
import os
import logging
from typing import Optional

# Setup logging
logger = logging.getLogger(__name__)

def build_vector_store(pdf_path: str = "Career_Advisor_Guide_2025.pdf", 
                      chunk_size: int = 500, 
                      chunk_overlap: int = 50,
                      persist_dir: str = "chroma_db") -> Optional[Chroma]:
    """
    Build a vector store from a PDF document.
    
    Args:
        pdf_path: Path to the PDF file
        chunk_size: Size of text chunks for splitting
        chunk_overlap: Overlap between consecutive chunks
        persist_dir: Directory to persist the vector store
        
    Returns:
        Chroma vector store or None if failed
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        Exception: For other processing errors
    """
    try:
        # Validate PDF file exists
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if not pdf_path.lower().endswith('.pdf'):
            raise ValueError(f"File must be a PDF: {pdf_path}")
        
        logger.info(f"Loading PDF: {pdf_path}")
        
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        
        if not docs:
            raise ValueError(f"No content found in PDF: {pdf_path}")
        
        logger.info(f"Loaded {len(docs)} pages from PDF")
        
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap
        )
        splits = splitter.split_documents(docs)
        
        if not splits:
            raise ValueError("No text chunks created from PDF")
        
        logger.info(f"Created {len(splits)} text chunks")
        
        # Initialize embeddings
        try:
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},  # Ensure CPU usage for compatibility
                encode_kwargs={'normalize_embeddings': True}
            )
            logger.info("Embeddings model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load embeddings model: {str(e)}")
            raise
        
        # Create vector store
        try:
            vectorstore = Chroma.from_documents(
                splits, 
                embeddings, 
                persist_directory=persist_dir
            )
            
            # Persist the vector store
            vectorstore.persist()
            logger.info(f"Vector store created and persisted to {persist_dir}")
            
            return vectorstore
            
        except Exception as e:
            logger.error(f"Failed to create vector store: {str(e)}")
            raise
            
    except FileNotFoundError:
        logger.error(f"PDF file not found: {pdf_path}")
        raise
    except ValueError as e:
        logger.error(f"Invalid input: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error building vector store: {str(e)}")
        raise

def load_existing_vector_store(persist_dir: str = "chroma_db") -> Optional[Chroma]:
    """
    Load an existing vector store from disk.
    
    Args:
        persist_dir: Directory where vector store is persisted
        
    Returns:
        Chroma vector store or None if not found
    """
    try:
        if not os.path.exists(persist_dir):
            logger.info(f"No existing vector store found at {persist_dir}")
            return None
        
        # Initialize embeddings (must match the one used during creation)
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Load existing vector store
        vectorstore = Chroma(
            persist_directory=persist_dir,
            embedding_function=embeddings
        )
        
        logger.info(f"Loaded existing vector store from {persist_dir}")
        return vectorstore
        
    except Exception as e:
        logger.error(f"Failed to load existing vector store: {str(e)}")
        return None
