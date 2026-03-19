# File: core/ufac_engine.py
import asyncio
import logging
from .fact_agent import extract_known_facts
from .assumption_agent import detect_assumptions
from .unknown_agent import detect_unknowns
from .confidence_agent import calculate_confidence
from .decision_agent import generate_next_steps
from .schema import UFACResponse
from data.pm_kisan_rules import PM_KISAN_RULES

logger = logging.getLogger(__name__)


class UFACError(Exception):
    """Base exception for UFAC engine errors."""
    pass

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
    """
    Run UFAC assessment with comprehensive error handling.
    
    Executes 5 agents in 2 batches with graceful fallbacks if any agent fails.
    """
    logger.info(f"Starting UFAC assessment with data: {list(user_data.keys())}")
    
    try:
        # Batch 1: Fact, Assumption, Unknown detection (parallel)
        logger.debug("Running Batch 1 agents (Fact, Assumption, Unknown)...")
        try:
            fact_result, assumption_result, unknown_result = await asyncio.gather(
                extract_known_facts(user_data),
                detect_assumptions(user_data),
                detect_unknowns(user_data, PM_KISAN_RULES),
                return_exceptions=True
            )
            
            # Handle exceptions from batch 1
            if isinstance(fact_result, Exception):
                logger.error(f"Fact agent failed: {str(fact_result)}", exc_info=fact_result)
                fact_result = {"facts": [], "consensus": 0.0}
            if isinstance(assumption_result, Exception):
                logger.error(f"Assumption agent failed: {str(assumption_result)}", exc_info=assumption_result)
                assumption_result = {"assumptions": [], "consensus": 0.0}
            if isinstance(unknown_result, Exception):
                logger.error(f"Unknown agent failed: {str(unknown_result)}", exc_info=unknown_result)
                unknown_result = {"unknowns": [], "consensus": 0.0}
                
        except Exception as e:
            logger.error(f"Batch 1 execution failed: {str(e)}", exc_info=True)
            fact_result = {"facts": [], "consensus": 0.0}
            assumption_result = {"assumptions": [], "consensus": 0.0}
            unknown_result = {"unknowns": [], "consensus": 0.0}

        known = fact_result.get("facts", [])
        fact_consensus = fact_result.get("consensus", 0.0)
        assumptions = assumption_result.get("assumptions", [])
        assumption_consensus = assumption_result.get("consensus", 0.0)
        unknowns = unknown_result.get("unknowns", [])
        unknown_consensus = unknown_result.get("consensus", 0.0)

        # Batch 2: Confidence and Decision (parallel)
        logger.debug("Running Batch 2 agents (Confidence, Decision)...")
        try:
            confidence_result, decision_result = await asyncio.gather(
                calculate_confidence(known, unknowns),
                generate_next_steps(unknowns),
                return_exceptions=True
            )
            
            # Handle exceptions from batch 2
            if isinstance(confidence_result, Exception):
                logger.error(f"Confidence agent failed: {str(confidence_result)}", exc_info=confidence_result)
                confidence_result = {"confidence": 50, "consensus": 0.0}
            if isinstance(decision_result, Exception):
                logger.error(f"Decision agent failed: {str(decision_result)}", exc_info=decision_result)
                decision_result = {"next_steps": [], "consensus": 0.0}
                
        except Exception as e:
            logger.error(f"Batch 2 execution failed: {str(e)}", exc_info=True)
            confidence_result = {"confidence": 50, "consensus": 0.0}
            decision_result = {"next_steps": [], "consensus": 0.0}

        confidence = int(confidence_result.get("confidence", 50))
        confidence_consensus = confidence_result.get("consensus", 0.0)
        next_steps = decision_result.get("next_steps", [])
        decision_consensus = decision_result.get("consensus", 0.0)

        risk = "HIGH" if confidence < 40 else "MEDIUM" if confidence < 70 else "LOW"
        answer = _determine_answer(confidence, unknowns, known)
        
        logger.info(f"UFAC assessment completed: confidence={confidence}, risk={risk}")

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
        
    except Exception as e:
        logger.error(f"UFAC assessment failed: {str(e)}", exc_info=True)
        raise UFACError(f"Assessment failed: {str(e)}") from e
