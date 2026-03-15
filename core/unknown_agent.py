import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def detect_unknowns(user_data, rules):
    prompt = f"""
You are the Unknown Detection Agent. Your task is to identify missing critical information required for PM-KISAN scheme eligibility.

User data: {json.dumps(user_data)}
Required fields from rules: {json.dumps(rules.get("required_fields", []))}
Disqualifiers: {json.dumps(rules.get("disqualifiers", []))}

Respond with a JSON object containing a list of unknowns:
{{"unknowns": ["missing field1", "missing field2", ...]}}

Focus on information that is essential but not provided.
"""
    responses = run_llm_council(prompt, num_runs=3)
    unknowns_lists = [resp.get("unknowns", []) for resp in responses]
    aggregated_unknowns = aggregate_list_responses(unknowns_lists)
    consensus = calculate_consensus(unknowns_lists)
    return {"unknowns": aggregated_unknowns, "consensus": consensus}
