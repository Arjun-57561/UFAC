import json
from .llm_utils import run_llm_council, aggregate_score_responses, calculate_consensus

def calculate_confidence(known, unknowns):
    prompt = f"""You are the Confidence Calibration Agent for PM-KISAN eligibility.

Your task: Calculate a confidence score (0-100) for the eligibility assessment.
- 0-30: Very low confidence (too many unknowns)
- 30-60: Low-medium confidence (significant gaps)
- 60-80: Medium-high confidence (minor gaps)
- 80-100: High confidence (mostly complete)

Known facts ({len(known)} total): {json.dumps(known)}
Unknowns ({len(unknowns)} total): {json.dumps(unknowns)}

Calculation guidance:
- Start at 100
- Subtract 20 per critical unknown
- Subtract 5 per minor unknown
- Add 5 per confirmed fact
- Apply judgment for overall reliability

Respond ONLY with valid JSON (no markdown, no extra text):
{{"confidence": 75}}

Provide a score reflecting assessment reliability.
"""
    responses = run_llm_council(prompt, num_runs=3)
    confidence_scores = [resp.get("confidence", 50) for resp in responses if isinstance(resp.get("confidence"), (int, float))]
    if not confidence_scores:
        confidence_scores = [50]  # Default if parsing fails
    aggregated_confidence = aggregate_score_responses(confidence_scores)
    consensus = calculate_consensus(confidence_scores)
    return {"confidence": aggregated_confidence, "consensus": consensus}
