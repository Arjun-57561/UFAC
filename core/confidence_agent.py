import json
from .llm_utils import run_llm_council, aggregate_score_responses, calculate_consensus

def calculate_confidence(known, unknowns):
    prompt = f"""
You are the Confidence Calibration Agent. Your task is to calculate a confidence score (0-100) for the eligibility assessment based on known facts and unknowns.

Known facts: {json.dumps(known)}
Unknowns: {json.dumps(unknowns)}

Formula suggestion: Start at 100, subtract 15 per unknown, add 10 per known fact. But use your judgment for a calibrated score.

Respond with a JSON object containing the confidence score:
{{"confidence": 75}}

Provide a score that reflects the reliability of the assessment.
"""
    responses = run_llm_council(prompt, num_runs=3)
    confidence_scores = [resp.get("confidence", 0) for resp in responses if isinstance(resp.get("confidence"), (int, float))]
    aggregated_confidence = aggregate_score_responses(confidence_scores)
    consensus = calculate_consensus(confidence_scores)
    return {"confidence": aggregated_confidence, "consensus": consensus}
