# File: core/unknown_agent.py
import json
import logging
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus
from data.rag_pipeline import get_retriever

logger = logging.getLogger(__name__)

async def detect_unknowns(user_data: dict, rules: dict) -> dict:
    required_fields = rules.get("required_fields", [])
    disqualifiers = rules.get("disqualifiers", {})
    mandatory = rules.get("mandatory_verifications", [])

    # Get RAG context (cached retriever)
    try:
        retriever = get_retriever()
        rag_docs = retriever.invoke("PM-KISAN required documents disqualifiers missing fields verification")
        rag_context = "\n".join([d.page_content for d in rag_docs])
    except Exception as e:
        logger.warning(f"RAG retrieval failed: {e}. Using empty context.")
        rag_context = ""

    prompt = f"""You are the Unknown Detection Agent for PM-KISAN eligibility.

Your task: Identify critical missing information needed for a confident eligibility assessment.
- Focus on required fields not provided
- Check for potential disqualifiers not addressed
- Include mandatory verification gaps

Official guidelines context:
{rag_context}

User data: {json.dumps(user_data)}
Required fields: {json.dumps(required_fields)}
Disqualifiers to check: {json.dumps(disqualifiers)}
Mandatory verifications: {json.dumps(mandatory)}

Respond ONLY with valid JSON (no markdown, no extra text):
{{"unknowns": ["missing_field1", "missing_field2", ...]}}

Examples:
- "Land ownership status not confirmed in land records"
- "e-KYC completion status unknown"
- "Annual income or tax-paying status not provided"
- "Pension amount not specified — disqualifier check pending"
"""
    responses = await run_llm_council(prompt, num_runs=3)
    unknowns_lists = [resp.get("unknowns", []) for resp in responses]
    return {
        "unknowns": aggregate_list_responses(unknowns_lists, threshold=0.4),
        "consensus": calculate_consensus(unknowns_lists)
    }
