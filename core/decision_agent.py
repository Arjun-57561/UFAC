import json
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus

def generate_next_steps(unknowns):
    prompt = f"""
You are the Decision Guidance Agent. Your task is to provide actionable next steps for the user based on the unknowns and overall assessment.

Unknowns: {json.dumps(unknowns)}

Respond with a JSON object containing a list of next steps:
{{"next_steps": ["step1", "step2", ...]}}

Make the steps practical and helpful for completing the PM-KISAN application.
"""
    responses = run_llm_council(prompt, num_runs=3)
    steps_lists = [resp.get("next_steps", []) for resp in responses]
    aggregated_steps = aggregate_list_responses(steps_lists)
    consensus = calculate_consensus(steps_lists)
    return {"next_steps": aggregated_steps, "consensus": consensus}
