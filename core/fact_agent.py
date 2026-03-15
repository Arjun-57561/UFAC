# UFAC/core/fact_agent.py
import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def extract_known_facts(user_data):
    prompt = f"""
You are the Fact Boundary Agent. Your task is to extract confirmed, objective facts from the user's provided data.
Only include information that is explicitly stated and verifiable.

User data: {json.dumps(user_data)}

Respond with a JSON object containing a list of facts:
{{"facts": ["fact1", "fact2", ...]}}

Be precise and avoid assumptions.
"""
    responses = run_llm_council(prompt, num_runs=3)
    facts_lists = [resp.get("facts", []) for resp in responses]
    aggregated_facts = aggregate_list_responses(facts_lists)
    consensus = calculate_consensus(facts_lists)
    return {"facts": aggregated_facts, "consensus": consensus}
