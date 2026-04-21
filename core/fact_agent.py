# File: core/fact_agent.py
import json
import logging
from .llm_utils import run_llm_council, aggregate_list_responses, calculate_consensus
from data.rag_pipeline import get_retriever

logger = logging.getLogger(__name__)

async def extract_known_facts(user_data: dict) -> dict:
    # Get RAG context (cached retriever)
    try:
        retriever = get_retriever()
        rag_docs = retriever.invoke(f"PM-KISAN facts eligibility {user_data}")
        rag_context = "\n".join([d.page_content for d in rag_docs])
    except Exception as e:
        logger.warning(f"RAG retrieval failed: {e}. Using empty context.")
        rag_context = ""
    
    prompt = f"""You are the Fact Boundary Agent for PM-KISAN eligibility assessment.

Your task: Extract ONLY confirmed, objective facts from the user's provided data.
- Include only explicitly stated information
- Avoid any assumptions or inferences
- Be specific and verifiable

Official guidelines context:
{rag_context}

User data: {json.dumps(user_data)}

Respond ONLY with valid JSON (no markdown, no extra text):
{{"facts": ["fact1", "fact2", ...]}}

Valid examples:
- "User is a farmer"
- "User owns 2 hectares of land"
- "User has Aadhaar number provided"

Invalid examples (do not include):
- "User likely owns land"
- "User probably has Aadhaar"
"""
    responses = await run_llm_council(prompt, num_runs=3)
    facts_lists = [resp.get("facts", []) for resp in responses]
    return {
        "facts": aggregate_list_responses(facts_lists, threshold=0.4),
        "consensus": calculate_consensus(facts_lists),
    }
