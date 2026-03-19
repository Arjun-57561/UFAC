# File: api/app.py
import logging
import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.llm_utils import init_gemini, LLMInitializationError, LLMError
from core.ufac_engine import run_ufac, UFACError
from core.schema import UFACResponse
from data.rag_pipeline import get_retriever, get_vectorstore_status, RAGError

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: Initialize Groq API and RAG pipeline. Shutdown: cleanup."""
    logger.info("="*70)
    logger.info("🚀 Starting UFAC Engine v2.0...")
    logger.info("="*70)
    
    # Initialize Groq API
    try:
        init_gemini()
        logger.info("✅ Groq API initialized successfully")
    except LLMInitializationError as e:
        logger.error(f"❌ Failed to initialize Groq API: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error during Groq initialization: {str(e)}", exc_info=True)
        raise
    
    # Initialize RAG pipeline
    rag_status = {"initialized": False, "error": None}
    try:
        logger.info("Initializing RAG pipeline...")
        retriever = get_retriever()
        status = get_vectorstore_status()
        
        if status.get("collection_count", 0) == 0:
            logger.warning("⚠️  RAG initialized but no chunks found")
            logger.info("Please run: python setup_rag.py")
            rag_status["warning"] = "No chunks indexed"
        else:
            logger.info(f"✅ RAG pipeline ready: {status['collection_count']} chunks indexed")
            rag_status["initialized"] = True
            
    except RAGError as e:
        logger.warning(f"⚠️  RAG pipeline initialization failed: {str(e)}")
        logger.info("Continuing without RAG (using hardcoded rules)")
        rag_status["error"] = str(e)
    except Exception as e:
        logger.warning(f"⚠️  Unexpected error during RAG initialization: {str(e)}", exc_info=True)
        logger.info("Continuing without RAG (using hardcoded rules)")
        rag_status["error"] = str(e)
    
    logger.info("="*70)
    logger.info("✅ UFAC Engine ready for requests")
    logger.info("="*70)
    
    # Store RAG status in app state for health checks
    app.state.rag_status = rag_status
    
    yield
    
    logger.info("🛑 UFAC Engine shutting down...")


app = FastAPI(
    title="UFAC Engine API",
    description="Unknown-Fact-Assumption-Confidence engine for PM-KISAN eligibility",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all HTTP requests and responses."""
    start_time = time.time()
    request_id = request.headers.get("x-request-id", "unknown")
    
    logger.info(f"[{request_id}] {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"[{request_id}] {response.status_code} - {process_time:.3f}s")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"[{request_id}] Request failed after {process_time:.3f}s: {str(e)}", exc_info=True)
        raise


class EligibilityCheckRequest(BaseModel):
    occupation: Optional[str] = None
    land_ownership: Optional[str] = None
    aadhaar_linked: Optional[bool] = None
    aadhaar_ekyc_done: Optional[bool] = None
    bank_account: Optional[bool] = None
    annual_income: Optional[float] = None
    income_tax_payer: Optional[bool] = None
    govt_employee: Optional[bool] = None
    pension_above_10k: Optional[bool] = None
    practicing_professional: Optional[bool] = None
    constitutional_post_holder: Optional[bool] = None
    state: Optional[str] = None
    district: Optional[str] = None
    additional_info: Optional[dict] = None


@app.get("/health")
async def health_check():
    """Health check with RAG status."""
    rag_status = getattr(app.state, "rag_status", {"initialized": False})
    return {
        "status": "healthy",
        "service": "UFAC Engine v2",
        "rag": rag_status
    }


@app.get("/rag-status")
async def rag_status_endpoint():
    """Check RAG pipeline status."""
    try:
        status = get_vectorstore_status()
        logger.info(f"RAG status check: {status}")
        return {"status": "ok", "rag": status}
    except RAGError as e:
        logger.error(f"RAG status check failed: {str(e)}")
        return {"status": "error", "error": str(e)}
    except Exception as e:
        logger.error(f"Unexpected error in RAG status check: {str(e)}", exc_info=True)
        return {"status": "error", "error": str(e)}


@app.post("/check", response_model=UFACResponse)
async def check_eligibility(request: EligibilityCheckRequest):
    """
    Check PM-KISAN eligibility.
    Runs all 5 agents with parallel async execution for low latency.
    """
    try:
        user_data = request.model_dump(exclude_none=True)
        logger.info(f"Processing eligibility check with fields: {list(user_data.keys())}")
        
        result = await run_ufac(user_data)
        logger.info(f"Eligibility check completed: confidence={result.confidence}, risk={result.risk_level}")
        return result
        
    except UFACError as e:
        logger.error(f"UFAC assessment failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Assessment failed: {str(e)}"
        )
    except LLMError as e:
        logger.error(f"LLM error during assessment: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail=f"LLM service error: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during eligibility check: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )


@app.get("/")
async def root():
    return {
        "service": "UFAC Engine — PM-KISAN Eligibility Assessment v2",
        "endpoints": {
            "health": "GET /health",
            "check": "POST /check",
            "rag_status": "GET /rag-status",
            "docs": "GET /docs",
        },
    }

