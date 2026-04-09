# File: data/rag_pipeline.py
# RAG Pipeline with ChromaDB + Singleton Retriever Caching

import os
import logging
from typing import Optional
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

logger = logging.getLogger(__name__)

DATA_DIR = os.path.dirname(__file__)
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")

# Singleton retriever cache
_retriever_cache: Optional[object] = None
_embeddings_cache: Optional[SentenceTransformerEmbeddings] = None


class RAGError(Exception):
    """Base exception for RAG-related errors."""
    pass


class RAGInitializationError(RAGError):
    """Raised when RAG initialization fails."""
    pass


class RAGRetrievalError(RAGError):
    """Raised when document retrieval fails."""
    pass

def _get_embeddings() -> SentenceTransformerEmbeddings:
    """Get or create embeddings model (cached) with error handling."""
    global _embeddings_cache
    if _embeddings_cache is None:
        try:
            logger.info("Loading SentenceTransformer embeddings model...")
            _embeddings_cache = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            logger.info("✅ Embeddings model loaded successfully")
        except Exception as e:
            error_msg = f"Failed to load embeddings model: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise RAGInitializationError(error_msg) from e
    return _embeddings_cache

def build_vectorstore() -> None:
    """Build ChromaDB vectorstore from PDFs in data/ directory with error handling."""
    logger.info("🔨 Building vectorstore from PDFs...")
    
    if not os.path.exists(DATA_DIR):
        error_msg = f"Data directory not found: {DATA_DIR}"
        logger.error(error_msg)
        raise RAGInitializationError(error_msg)
    
    # Check if PDFs exist
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
    if not pdf_files:
        warning_msg = f"⚠️  No PDF files found in {DATA_DIR}"
        logger.warning(warning_msg)
        logger.info("Please add PM-KISAN guideline PDFs to the data/ directory")
        raise RAGInitializationError(warning_msg)
    
    logger.info(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    
    try:
        # Load PDFs
        logger.info("Loading PDFs...")
        loader = PyPDFDirectoryLoader(DATA_DIR)
        docs = loader.load()
        logger.info(f"✅ Loaded {len(docs)} pages from PDFs")
        
        if not docs:
            error_msg = "No documents loaded from PDFs"
            logger.error(error_msg)
            raise RAGInitializationError(error_msg)
        
        # Split into chunks
        logger.info("Splitting documents into chunks...")
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        chunks = splitter.split_documents(docs)
        logger.info(f"✅ Split into {len(chunks)} chunks")
        
        if not chunks:
            error_msg = "No chunks created from documents"
            logger.error(error_msg)
            raise RAGInitializationError(error_msg)
        
        # Create vectorstore
        logger.info("Creating vectorstore...")
        embeddings = _get_embeddings()
        db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory=CHROMA_DIR
        )
        db.persist()
        logger.info(f"✅ Indexed {len(chunks)} chunks into ChromaDB at {CHROMA_DIR}")
        
    except RAGInitializationError:
        raise
    except Exception as e:
        error_msg = f"Failed to build vectorstore: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise RAGInitializationError(error_msg) from e

def get_retriever(force_rebuild: bool = False):
    """
    Get or create retriever (singleton pattern with caching).
    
    Args:
        force_rebuild: If True, rebuild vectorstore from PDFs
    
    Returns:
        Chroma retriever object
        
    Raises:
        RAGInitializationError: If retriever cannot be initialized
    """
    global _retriever_cache
    
    # Force rebuild if requested
    if force_rebuild:
        logger.info("🔄 Force rebuilding vectorstore...")
        _retriever_cache = None
        build_vectorstore()
    
    # Return cached retriever if available
    if _retriever_cache is not None:
        logger.debug("Using cached retriever")
        return _retriever_cache
    
    # Check if ChromaDB exists
    if not os.path.exists(CHROMA_DIR):
        logger.warning(f"ChromaDB not found at {CHROMA_DIR}")
        logger.info("Building vectorstore for the first time...")
        build_vectorstore()
    
    # Load from disk
    try:
        logger.info("Loading retriever from ChromaDB...")
        embeddings = _get_embeddings()
        db = Chroma(
            persist_directory=CHROMA_DIR,
            embedding_function=embeddings
        )
        _retriever_cache = db.as_retriever(search_kwargs={"k": 4})
        logger.info("✅ Retriever loaded and cached")
        return _retriever_cache
    except Exception as e:
        error_msg = f"Failed to load retriever from ChromaDB: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise RAGInitializationError(error_msg) from e

def clear_cache() -> None:
    """Clear the retriever cache (useful for testing)."""
    global _retriever_cache, _embeddings_cache
    _retriever_cache = None
    _embeddings_cache = None
    logger.info("Cache cleared")

def get_vectorstore_status() -> dict:
    """Get status of vectorstore (for health checks)."""
    status = {
        "chroma_exists": os.path.exists(CHROMA_DIR),
        "chroma_path": CHROMA_DIR,
        "retriever_cached": _retriever_cache is not None,
        "embeddings_cached": _embeddings_cache is not None,
    }
    
    if status["chroma_exists"]:
        try:
            embeddings = _get_embeddings()
            db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)
            status["collection_count"] = db._collection.count()
        except Exception as e:
            status["error"] = str(e)
    
    return status


def _get_fallback_context() -> str:
    """Fallback context when RAG is unavailable."""
    return """
PM-KISAN Eligibility (Fallback Rules):
- Beneficiary: Small/marginal farmers with cultivable land
- Required: Valid Aadhaar, bank account, e-KYC completion
- Disqualified: Income tax payers, govt employees,
  pension > Rs 10,000/month, practicing professionals,
  constitutional post holders, institutional landholders
- Land: Must be in state/UT land records as of Feb 1, 2019
- Payment: Rs 6,000/year in 3 installments of Rs 2,000 each
"""


def retrieve_context(query: str, k: int = 4) -> str:
    """
    Retrieve context from RAG pipeline with graceful fallback.
    
    Args:
        query: Search query
        k: Number of documents to retrieve
        
    Returns:
        Retrieved context or fallback rules
    """
    try:
        retriever = get_retriever()
        retriever.search_kwargs["k"] = k
        docs = retriever.invoke(query)
        if not docs:
            logger.warning("No documents retrieved, using fallback context")
            return _get_fallback_context()
        return "\n\n---\n\n".join(
            f"[Source: {doc.metadata.get('source','Unknown')}, "
            f"Page {doc.metadata.get('page','?')}]\n{doc.page_content}"
            for doc in docs
        )
    except Exception as e:
        logger.warning(f"RAG failed, using fallback context: {e}")
        return _get_fallback_context()
