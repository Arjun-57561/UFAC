# File: core/schema.py
# UFAC/core/schema.py
from pydantic import BaseModel, Field
from typing import List, Literal

class UFACResponse(BaseModel):
    answer: str
    confidence: int = Field(..., ge=0, le=100)

    known_facts: List[str]
    assumptions: List[str]
    unknowns: List[str]

    risk_level: Literal["LOW", "MEDIUM", "HIGH"]
    next_steps: List[str]

    # Per-agent consensus scores
    fact_consensus: float
    assumption_consensus: float
    unknown_consensus: float
    confidence_consensus: float
    decision_consensus: float
