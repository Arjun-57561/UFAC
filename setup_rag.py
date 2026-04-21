# File: setup_rag.py
"""
Setup script to initialize RAG pipeline.
Run this once after adding PM-KISAN PDF files to the data/ directory.

Usage:
    python setup_rag.py
"""

import sys
import logging
from data.rag_pipeline import build_vectorstore, get_vectorstore_status

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("="*60)
    logger.info("🚀 UFAC Engine - RAG Setup")
    logger.info("="*60)
    
    try:
        # Build vectorstore
        build_vectorstore()
        
        # Check status
        status = get_vectorstore_status()
        logger.info(f"\n✅ RAG Setup Complete!")
        logger.info(f"Status: {status}")
        
        if status.get("collection_count", 0) > 0:
            logger.info(f"✅ {status['collection_count']} chunks indexed and ready")
        else:
            logger.warning("⚠️  No chunks found. Please add PM-KISAN PDF files to data/")
        
        return 0
    except Exception as e:
        logger.error(f"❌ Setup failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
