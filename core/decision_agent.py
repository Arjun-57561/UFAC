# File: core/decision_agent.py
import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def generate_next_steps(unknowns):
    prompt = f"""You are the Decision Guidance Agent for PM-KISAN eligibility.

Your task: Provide actionable next steps based on unknowns and assessment gaps.
- Make steps practical and specific
- Prioritize critical information gathering
- Include document/verification requirements
- Focus on PM-KISAN application process

Unknowns to address ({len(unknowns)} total): {json.dumps(unknowns)}

Respond ONLY with valid JSON (no markdown, no extra text):
{{"next_steps": ["step1", "step2", ...]}}

Examples:
- "Verify land ownership with revenue records"
- "Link Aadhaar to bank account"
- "Gather income proof documents"
- "Register with local agricultural office"
"""
    responses = run_llm_council(prompt, num_runs=3)
    steps_lists = [resp.get("next_steps", []) for resp in responses]
    aggregated_steps = aggregate_list_responses(steps_lists, threshold=0.4)
    consensus = calculate_consensus(steps_lists)
    return {"next_steps": aggregated_steps, "consensus": consensus}
