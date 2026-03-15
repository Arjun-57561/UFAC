# File: core/schema.py
# This prevents scope creep.
# UFAC/core/schema.py
from pydantic import BaseModel
from typing import List

class UFACResponse(BaseModel):
    answer: str
    confidence: int  # 0–100

    known_facts: List[str]
    assumptions: List[str]
    unknowns: List[str]

    risk_level: str  # LOW / MEDIUM / HIGH
    next_steps: List[str]

    # Consensus scores for each agent
    fact_consensus: float
    assumption_consensus: float
    unknown_consensus: float
    confidence_consensus: float
    decision_consensus: float
