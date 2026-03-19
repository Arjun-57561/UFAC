# File: core/assumption_agent.py
import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

async def detect_assumptions(user_data: dict) -> dict:
    prompt = f"""You are the Assumption Detection Agent for PM-KISAN eligibility.

Your task: Identify implicit assumptions being made based on missing data.
- List assumptions that could affect eligibility
- Be specific about what is being assumed
- Focus on PM-KISAN relevant assumptions

User data: {json.dumps(user_data)}

PM-KISAN Context:
- Requires land ownership recorded in state/UT land records
- e-KYC via Aadhaar is mandatory (since 2023)
- Requires active bank account linked to Aadhaar
- Requires farmer status
- Disqualifiers: income tax payer, govt employee, pension > ₹10k/month,
  practicing professionals (doctors, lawyers, CAs, engineers),
  constitutional post holders, institutional landholders

Respond ONLY with valid JSON (no markdown, no extra text):
{{"assumptions": ["assumption1", "assumption2", ...]}}
"""
    responses = await run_llm_council(prompt, num_runs=3)
    assumptions_lists = [resp.get("assumptions", []) for resp in responses]
    return {
        "assumptions": aggregate_list_responses(assumptions_lists, threshold=0.4),
        "consensus": calculate_consensus(assumptions_lists),
    }
