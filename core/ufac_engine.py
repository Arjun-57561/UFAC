# File: core/ufac_engine.py
import asyncio
from .fact_agent import extract_known_facts
from .assumption_agent import detect_assumptions
from .unknown_agent import detect_unknowns
from .confidence_agent import calculate_confidence
from .decision_agent import generate_next_steps
from .schema import UFACResponse
from data.pm_kisan_rules import PM_KISAN_RULES

def _determine_answer(confidence: int, unknowns: list, known_facts: list) -> str:
    unknown_lower = " ".join(unknowns).lower()
    facts_lower = " ".join(known_facts).lower()

    # Hard disqualifier signals in known facts
    disqualifier_keywords = [
        "income tax", "government employee", "govt employee",
        "pension above", "constitutional post", "institutional landholder",
        "practicing professional",
    ]
    for kw in disqualifier_keywords:
        if kw in facts_lower:
            return f"Likely INELIGIBLE — disqualifier detected: {kw}"

    if confidence >= 80 and len(unknowns) == 0:
        return "Likely ELIGIBLE for PM-KISAN — all key criteria appear satisfied"
    elif confidence >= 65 and len(unknowns) <= 2:
        return "Possibly eligible — minor verifications pending"
    elif "e-kyc" in unknown_lower or "aadhaar" in unknown_lower:
        return "Cannot confirm — e-KYC / Aadhaar verification is mandatory and missing"
    elif "land" in unknown_lower:
        return "Cannot confirm — land ownership status not verified"
    else:
        return "Eligibility cannot be confirmed — too many unknowns"

async def run_ufac(user_data: dict) -> UFACResponse:
    # Run fact, assumption, and unknown detection in parallel
    fact_result, assumption_result, unknown_result = await asyncio.gather(
        extract_known_facts(user_data),
        detect_assumptions(user_data),
        detect_unknowns(user_data, PM_KISAN_RULES),
    )

    known = fact_result["facts"]
    fact_consensus = fact_result["consensus"]
    assumptions = assumption_result["assumptions"]
    assumption_consensus = assumption_result["consensus"]
    unknowns = unknown_result["unknowns"]
    unknown_consensus = unknown_result["consensus"]

    # Confidence and decision can now run in parallel too
    confidence_result, decision_result = await asyncio.gather(
        calculate_confidence(known, unknowns),
        generate_next_steps(unknowns),
    )

    confidence = int(confidence_result["confidence"])
    confidence_consensus = confidence_result["consensus"]
    next_steps = decision_result["next_steps"]
    decision_consensus = decision_result["consensus"]

    risk = "HIGH" if confidence < 40 else "MEDIUM" if confidence < 70 else "LOW"
    answer = _determine_answer(confidence, unknowns, known)

    return UFACResponse(
        answer=answer,
        confidence=confidence,
        known_facts=known,
        assumptions=assumptions,
        unknowns=unknowns,
        risk_level=risk,
        next_steps=next_steps,
        fact_consensus=fact_consensus,
        assumption_consensus=assumption_consensus,
        unknown_consensus=unknown_consensus,
        confidence_consensus=confidence_consensus,
        decision_consensus=decision_consensus,
    )
