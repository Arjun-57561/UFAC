# File: core/decision_agent.py
import json
import logging
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus
from data.rag_pipeline import get_retriever

logger = logging.getLogger(__name__)

async def generate_next_steps(unknowns: list) -> dict:
    # Get RAG context (cached retriever)
    try:
        retriever = get_retriever()
        rag_docs = retriever.invoke("PM-KISAN application process steps documents required e-KYC")
        rag_context = "\n".join([d.page_content for d in rag_docs])
    except Exception as e:
        logger.warning(f"RAG retrieval failed: {e}. Using empty context.")
        rag_context = ""
    
    prompt = f"""You are the Decision Guidance Agent for PM-KISAN eligibility.

Your task: Provide actionable next steps based on missing information and assessment gaps.
- Make steps practical, specific, and ordered by priority
- Include document/verification requirements
- Focus on PM-KISAN application and e-KYC process

Official guidelines context:
{rag_context}

Unknowns to address ({len(unknowns)} total): {json.dumps(unknowns)}

Respond ONLY with valid JSON (no markdown, no extra text):
{{"next_steps": ["step1", "step2", ...]}}

Examples:
- "Complete e-KYC via Aadhaar on pmkisan.gov.in or nearest CSC"
- "Verify land ownership in state revenue/land records"
- "Link Aadhaar to bank account at your bank branch"
- "Obtain income certificate to confirm non-tax-payer status"
- "Register with local Patwari or agricultural office"
"""
    responses = await run_llm_council(prompt, num_runs=3)
    steps_lists = [resp.get("next_steps", []) for resp in responses]
    return {
        "next_steps": aggregate_list_responses(steps_lists, threshold=0.4),
        "consensus": calculate_consensus(steps_lists),
    }
