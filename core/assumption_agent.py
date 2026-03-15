# File: core/assumption_agent.py
import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def detect_assumptions(user_data):
    prompt = f"""You are the Assumption Detection Agent for PM-KISAN eligibility.

Your task: Identify implicit assumptions being made based on missing data.
- List assumptions that could affect eligibility
- Be specific about what is being assumed
- Focus on PM-KISAN relevant assumptions

User data: {json.dumps(user_data)}

PM-KISAN Context:
- Requires land ownership (not stated = assumption needed)
- Requires Aadhaar linkage (not stated = assumption needed)
- Requires bank account (not stated = assumption needed)
- Requires farmer status (not stated = assumption needed)

Respond ONLY with valid JSON (no markdown, no extra text):
{{"assumptions": ["assumption1", "assumption2", ...]}}

Examples:
- "Assuming user owns agricultural land"
- "Assuming Aadhaar is linked to bank account"
- "Assuming user is registered as farmer"
"""
    responses = run_llm_council(prompt, num_runs=3)
    assumptions_lists = [resp.get("assumptions", []) for resp in responses]
    aggregated_assumptions = aggregate_list_responses(assumptions_lists, threshold=0.4)
    consensus = calculate_consensus(assumptions_lists)
    return {"assumptions": aggregated_assumptions, "consensus": consensus}
