import os
import asyncio
import json
import logging
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
from tenacity import (
    retry, stop_after_attempt, wait_exponential,
    retry_if_exception_type, before_sleep_log
)

load_dotenv()
logger = logging.getLogger(__name__)

MODEL_NAME = "llama-3.3-70b-versatile"
_client: Groq | None = None
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT_SECONDS", "15.0"))


class LLMError(Exception):
    """Base exception for LLM-related errors."""
    pass


class LLMInitializationError(LLMError):
    """Raised when LLM client initialization fails."""
    pass


class LLMCallError(LLMError):
    """Raised when an LLM API call fails."""
    pass


def init_gemini():  # Keep name for compatibility
    """Initialize Groq API client with error handling."""
    global _client
    try:
        key = os.getenv("GROQ_API_KEY")
        if not key:
            error_msg = "GROQ_API_KEY environment variable not set. Please add it to .env file."
            logger.error(error_msg)
            raise LLMInitializationError(error_msg)
        
        _client = Groq(api_key=key)
        logger.info("✅ Groq API initialized successfully with model: %s", MODEL_NAME)
    except Exception as e:
        error_msg = f"Failed to initialize Groq API: {str(e)}"
        logger.error(error_msg, exc_info=True)
        raise LLMInitializationError(error_msg) from e


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(Exception),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    reraise=True
)
def _call_groq_sync(client, prompt: str, temperature: float) -> str:
    """Synchronous Groq API call with tenacity retry logic."""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=min(temperature, 1.0),
        max_tokens=500,
    )
    return response.choices[0].message.content.strip()


async def _single_llm_call(prompt: str, temperature: float, run_index: int) -> Dict[str, Any]:
    """Execute a single LLM call with retry logic and error handling."""
    if _client is None:
        error_msg = "Groq client not initialized. Call init_gemini() first."
        logger.error(error_msg)
        raise LLMCallError(error_msg)

    from .circuit_breaker import groq_circuit_breaker
    
    if groq_circuit_breaker.is_open():
        logger.warning("Circuit breaker OPEN — skipping Groq call")
        return {}

    loop = asyncio.get_running_loop()
    
    try:
        logger.debug(f"Run {run_index+1} starting")
        result = await asyncio.wait_for(
            loop.run_in_executor(None, lambda: _call_groq_sync(_client, prompt, temperature)),
            timeout=LLM_TIMEOUT
        )
        groq_circuit_breaker.call_succeeded()
        logger.debug(f"Run {run_index+1} succeeded")
        return extract_json_from_response(result)
    except Exception as e:
        groq_circuit_breaker.call_failed()
        logger.error(f"LLM call failed: {e}")
        return {}


# All functions below stay exactly the same as before
async def run_llm_council(prompt: str, num_runs: int = 3) -> List[Dict[str, Any]]:
    """Run LLM council with configurable runs (respects DEV_MODE)."""
    if os.getenv("DEV_MODE", "false").lower() == "true":
        num_runs = 1
        logger.debug("DEV_MODE: using 1 LLM run")
    
    tasks = [
        _single_llm_call(prompt, temperature=0.7 + (i * 0.1), run_index=i)
        for i in range(num_runs)
    ]
    return await asyncio.gather(*tasks)


def extract_json_from_response(text: str) -> Dict[str, Any]:
    """Extract JSON from LLM response with error handling."""
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        logger.debug(f"Direct JSON parse failed: {str(e)}")
        
        # Try to extract JSON from markdown code blocks
        for marker in ["```json", "```"]:
            if marker in text:
                start = text.find(marker) + len(marker)
                end = text.find("```", start)
                if end > start:
                    try:
                        extracted = text[start:end].strip()
                        result = json.loads(extracted)
                        logger.debug("Successfully extracted JSON from code block")
                        return result
                    except json.JSONDecodeError:
                        logger.debug(f"Failed to parse extracted JSON from {marker} block")
        
        logger.warning(f"Could not parse JSON from LLM response. Raw text: {text[:200]}...")
        return {}


def aggregate_list_responses(responses: List[List[str]], threshold: float = 0.4) -> List[str]:
    if not responses:
        return []
    all_items: Dict[str, int] = {}
    total_runs = len(responses)
    for resp in responses:
        for item in resp:
            all_items[item] = all_items.get(item, 0) + 1
    return [item for item, count in all_items.items() if count / total_runs >= threshold]


def aggregate_score_responses(scores: List[float]) -> float:
    return sum(scores) / len(scores) if scores else 0.0


def calculate_consensus(responses: List[Any]) -> float:
    if not responses:
        return 0.0
    from collections import Counter
    non_empty = [r for r in responses if r]
    if not non_empty:
        return 0.0
    counts = Counter(str(r) for r in non_empty)
    return max(counts.values()) / len(non_empty)
