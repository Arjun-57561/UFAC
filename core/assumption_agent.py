import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def detect_assumptions(user_data):
    prompt = f"""
You are the Assumption Agent. Your task is to identify implicit assumptions being made based on the user's data and the context of PM-KISAN scheme eligibility.

User data: {json.dumps(user_data)}

Common assumptions for PM-KISAN:
- If land ownership is not specified, assume the user owns land.
- If Aadhaar linkage is not mentioned, assume it is linked.
- Other implicit assumptions based on missing data.

Respond with a JSON object containing a list of assumptions:
{{"assumptions": ["assumption1", "assumption2", ...]}}

Only include reasonable assumptions that could affect eligibility.
"""
    responses = run_llm_council(prompt, num_runs=3)
    assumptions_lists = [resp.get("assumptions", []) for resp in responses]
    aggregated_assumptions = aggregate_list_responses(assumptions_lists)
    consensus = calculate_consensus(assumptions_lists)
    return {"assumptions": aggregated_assumptions, "consensus": consensus}
