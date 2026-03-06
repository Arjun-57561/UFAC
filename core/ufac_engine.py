from .fact_agent import extract_known_facts
from .assumption_agent import detect_assumptions
from .unknown_agent import detect_unknowns
from .confidence_agent import calculate_confidence
from .decision_agent import generate_next_steps

from data.pm_kisan_rules import PM_KISAN_RULES
from core.schema import UFACResponse


def run_ufac(user_data):
    known = extract_known_facts(user_data)
    assumptions = detect_assumptions(user_data)
    unknowns = detect_unknowns(user_data, PM_KISAN_RULES)

    confidence = calculate_confidence(known, unknowns)

    if confidence < 40:
        risk = "HIGH"
    elif confidence < 70:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    next_steps = generate_next_steps(unknowns)

    return UFACResponse(
        answer="Eligibility cannot be confirmed yet",
        confidence=confidence,
        known_facts=known,
        assumptions=assumptions,
        unknowns=unknowns,
        risk_level=risk,
        next_steps=next_steps
    )
