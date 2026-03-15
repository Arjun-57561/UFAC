# File: core/ufac_engine.py
from .fact_agent import extract_known_facts
from .assumption_agent import detect_assumptions
from .unknown_agent import detect_unknowns
from .confidence_agent import calculate_confidence
from .decision_agent import generate_next_steps

from data.pm_kisan_rules import PM_KISAN_RULES
from core.schema import UFACResponse


def run_ufac(user_data):
    fact_result = extract_known_facts(user_data)
    known = fact_result["facts"]
    fact_consensus = fact_result["consensus"]

    assumption_result = detect_assumptions(user_data)
    assumptions = assumption_result["assumptions"]
    assumption_consensus = assumption_result["consensus"]

    unknown_result = detect_unknowns(user_data, PM_KISAN_RULES)
    unknowns = unknown_result["unknowns"]
    unknown_consensus = unknown_result["consensus"]

    confidence_result = calculate_confidence(known, unknowns)
    confidence = int(confidence_result["confidence"])
    confidence_consensus = confidence_result["consensus"]

    if confidence < 40:
        risk = "HIGH"
    elif confidence < 70:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    decision_result = generate_next_steps(unknowns)
    next_steps = decision_result["next_steps"]
    decision_consensus = decision_result["consensus"]

    return UFACResponse(
        answer="Eligibility cannot be confirmed yet",
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
        decision_consensus=decision_consensus
    )
