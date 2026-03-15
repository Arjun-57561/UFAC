# File: core/fact_agent.py
# UFAC/core/fact_agent.py
import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def extract_known_facts(user_data):
    prompt = f"""You are the Fact Boundary Agent for PM-KISAN eligibility assessment.

Your task: Extract ONLY confirmed, objective facts from the user's provided data.
- Include only explicitly stated information
- Avoid any assumptions or inferences
- Be specific and verifiable

User data: {json.dumps(user_data)}

Respond ONLY with valid JSON (no markdown, no extra text):
{{"facts": ["fact1", "fact2", ...]}}

Examples of valid facts:
- "User is a farmer"
- "User owns 2 hectares of land"
- "User has Aadhaar number provided"

Examples of invalid facts (assumptions):
- "User likely owns land" (not stated)
- "User probably has Aadhaar" (not confirmed)
"""
    responses = run_llm_council(prompt, num_runs=3)
    facts_lists = [resp.get("facts", []) for resp in responses]
    aggregated_facts = aggregate_list_responses(facts_lists, threshold=0.4)
    consensus = calculate_consensus(facts_lists)
    return {"facts": aggregated_facts, "consensus": consensus}
