# File: core/unknown_agent.py
import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def detect_unknowns(user_data, rules):
    required_fields = rules.get("required_fields", [])
    disqualifiers = rules.get("disqualifiers", [])
    
    prompt = f"""You are the Unknown Detection Agent for PM-KISAN eligibility.

Your task: Identify critical missing information needed for eligibility assessment.
- Focus on required fields not provided
- Check for potential disqualifiers
- List unknowns that prevent confident assessment

User data: {json.dumps(user_data)}
Required fields: {json.dumps(required_fields)}
Disqualifiers to check: {json.dumps(disqualifiers)}

Respond ONLY with valid JSON (no markdown, no extra text):
{{"unknowns": ["missing_field1", "missing_field2", ...]}}

Examples:
- "Land ownership status unknown"
- "Aadhaar linkage status not provided"
- "Annual income not specified"
"""
    responses = run_llm_council(prompt, num_runs=3)
    unknowns_lists = [resp.get("unknowns", []) for resp in responses]
    aggregated_unknowns = aggregate_list_responses(unknowns_lists, threshold=0.4)
    consensus = calculate_consensus(unknowns_lists)
    return {"unknowns": aggregated_unknowns, "consensus": consensus}
