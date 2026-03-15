from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from core.ufac_engine import run_ufac
from core.schema import UFACResponse
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="UFAC Engine API",
    description="Unknown-Fact-Assumption-Confidence engine for PM-KISAN eligibility",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EligibilityCheckRequest(BaseModel):
    """Request model for eligibility check"""
    occupation: Optional[str] = None
    land_ownership: Optional[str] = None
    aadhaar_linked: Optional[bool] = None
    bank_account: Optional[bool] = None
    annual_income: Optional[float] = None
    state: Optional[str] = None
    district: Optional[str] = None
    additional_info: Optional[dict] = None

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "UFAC Engine"}

@app.post("/check", response_model=UFACResponse)
def check_eligibility(request: EligibilityCheckRequest):
    """
    Check PM-KISAN eligibility based on provided information.
    
    Returns:
    - answer: Eligibility status
    - confidence: Confidence score (0-100)
    - known_facts: Extracted facts
    - assumptions: Identified assumptions
    - unknowns: Missing information
    - risk_level: Assessment risk level
    - next_steps: Recommended actions
    - consensus scores for each agent
    """
    try:
        user_data = request.model_dump(exclude_none=True)
        logger.info(f"Processing eligibility check for: {user_data}")
        result = run_ufac(user_data)
        return result
    except Exception as e:
        logger.error(f"Error in eligibility check: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/")
def root():
    """API documentation"""
    return {
        "service": "UFAC Engine - PM-KISAN Eligibility Assessment",
        "endpoints": {
            "health": "/health",
            "check": "/check (POST)",
            "docs": "/docs"
        }
    }

