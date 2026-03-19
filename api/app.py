# File: api/app.py
import logging
import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from core.llm_utils import init_gemini
from core.ufac_engine import run_ufac
from core.schema import UFACResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: validate env and initialize Gemini. Shutdown: cleanup."""
    logger.info("Starting UFAC Engine — initializing Gemini...")
    init_gemini()  # Fails fast at startup if API key missing
    yield
    logger.info("UFAC Engine shutting down.")

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

# Serve the UI static files
ui_dir = os.path.join(os.path.dirname(__file__), "..", "ui")
if os.path.isdir(ui_dir):
    app.mount("/ui", StaticFiles(directory=ui_dir), name="ui")

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
    return {"status": "healthy", "service": "UFAC Engine v2"}

@app.post("/check", response_model=UFACResponse)
async def check_eligibility(request: EligibilityCheckRequest):
    """
    Check PM-KISAN eligibility.
    Runs all 5 agents with parallel async execution for low latency.
    """
    try:
        user_data = request.model_dump(exclude_none=True)
        logger.info(f"Processing eligibility check: {user_data}")
        result = await run_ufac(user_data)
        return result
    except Exception as e:
        logger.error(f"Eligibility check failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
async def root():
    ui_path = os.path.join(os.path.dirname(__file__), "..", "ui", "index.html")
    if os.path.isfile(ui_path):
        return FileResponse(ui_path, media_type="text/html")
    return {
        "service": "UFAC Engine — PM-KISAN Eligibility Assessment v2",
        "endpoints": {
            "health": "GET /health",
            "check": "POST /check",
            "docs": "GET /docs",
            "ui": "GET /ui/index.html",
        },
    }

