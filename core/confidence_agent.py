# File: core/confidence_agent.py
import json
from .llm_utils import run_llm_council, aggregate_score_responses, calculate_consensus

async def calculate_confidence(known: list, unknowns: list) -> dict:
    prompt = f"""You are the Confidence Calibration Agent for PM-KISAN eligibility.

Your task: Calculate a confidence score (0-100) for the eligibility assessment.
- 0-30: Very low confidence (too many unknowns)
- 30-60: Low-medium confidence (significant gaps)
- 60-80: Medium-high confidence (minor gaps)
- 80-100: High confidence (mostly complete data)

Known facts ({len(known)} total): {json.dumps(known)}
Unknowns ({len(unknowns)} total): {json.dumps(unknowns)}

Calculation guidance:
- Start at 100
- Subtract 20 per critical unknown (land, Aadhaar e-KYC, disqualifier status)
- Subtract 5 per minor unknown
- Add 5 per confirmed eligibility-relevant fact
- Apply holistic judgment for reliability

Respond ONLY with valid JSON (no markdown, no extra text):
{{"confidence": 75}}
"""
    responses = await run_llm_council(prompt, num_runs=3)
    scores = [
        resp.get("confidence")
        for resp in responses
        if isinstance(resp.get("confidence"), (int, float))
    ]
    if not scores:
        scores = [50]
    return {
        "confidence": aggregate_score_responses(scores),
        "consensus": calculate_consensus(scores),
    }
