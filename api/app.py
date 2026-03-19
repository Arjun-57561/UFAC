# File: api/app.py
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator

from core.llm_utils import init_groq
from core.ufac_engine import run_ufac
from core.schema import UFACResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: validate env and initialize Groq. Shutdown: cleanup."""
    logger.info("Starting UFAC Engine — initializing Groq...")
    init_groq()  # Fails fast at startup if API key missing
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Attach X-Process-Time (ms) and X-Request-ID headers to every response."""
    request_id = str(uuid.uuid4())
    start = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start) * 1000
    response.headers["X-Process-Time"] = f"{elapsed_ms:.2f}ms"
    response.headers["X-Request-ID"] = request_id
    return response


class EligibilityCheckRequest(BaseModel):
    occupation: Optional[str] = Field(None, max_length=100)
    land_ownership: Optional[str] = Field(None, max_length=50)
    aadhaar_linked: Optional[bool] = None
    aadhaar_ekyc_done: Optional[bool] = None
    bank_account: Optional[bool] = None
    annual_income: Optional[float] = Field(None, ge=0)
    income_tax_payer: Optional[bool] = None
    govt_employee: Optional[bool] = None
    pension_above_10k: Optional[bool] = None
    practicing_professional: Optional[bool] = None
    constitutional_post_holder: Optional[bool] = None
    state: Optional[str] = Field(None, max_length=100)
    district: Optional[str] = Field(None, max_length=100)
    additional_info: Optional[dict] = None

    @field_validator("occupation", "land_ownership", "state", "district", mode="before")
    @classmethod
    def strip_and_nullify_blank(cls, v):
        if v is None:
            return v
        if not isinstance(v, str):
            raise ValueError("must be a string")
        v = v.strip()
        if v == "":
            return None
        return v

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
    return {
        "service": "UFAC Engine — PM-KISAN Eligibility Assessment v2",
        "endpoints": {
            "health": "GET /health",
            "check": "POST /check",
            "docs": "GET /docs",
        },
    }

