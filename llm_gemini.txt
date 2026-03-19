# File: core/llm_utils.py
import os
import asyncio
import json
import logging
from typing import List, Dict, Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()  # Loads .env file automatically

logger = logging.getLogger(__name__)

MODEL_NAME = "gemini-1.5-flash-8b"  # Free tier: 1500 req/day vs 500 for 2.0-flash

_client: genai.Client | None = None  # Singleton client


def init_gemini():
    global _client
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    _client = genai.Client(api_key=key)
    logger.info("Gemini API initialized successfully.")


async def _single_llm_call(prompt: str, temperature: float, run_index: int) -> Dict[str, Any]:
    """Single async Gemini call with timeout and retry."""
    if _client is None:
        raise RuntimeError("Gemini client not initialized. Call init_gemini() first.")

    def _call():
        response = _client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=temperature,
                max_output_tokens=500,
                top_p=0.95,
            ),
        )
        return response.text.strip()

    loop = asyncio.get_running_loop()  # ✅ correct for Python 3.10+

    for attempt in range(2):
        try:
            text = await asyncio.wait_for(
                loop.run_in_executor(None, _call),
                timeout=15.0,
            )
            return extract_json_from_response(text)
        except (asyncio.TimeoutError, Exception) as e:
            logger.warning(f"Run {run_index+1} attempt {attempt+1} failed: {e}")
            await asyncio.sleep(0.5 * (attempt + 1))  # backoff before retry

    return {}


async def run_llm_council(prompt: str, num_runs: int = 3) -> List[Dict[str, Any]]:
    """Run Gemini LLM concurrently num_runs times for diversity and consensus."""
    tasks = [
        _single_llm_call(prompt, temperature=0.7 + (i * 0.1), run_index=i)
        for i in range(num_runs)
    ]
    return await asyncio.gather(*tasks)


def extract_json_from_response(text: str) -> Dict[str, Any]:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        for marker in ["```json", "```"]:
            if marker in text:
                start = text.find(marker) + len(marker)
                end = text.find("```", start)
                if end > start:
                    try:
                        return json.loads(text[start:end].strip())
                    except json.JSONDecodeError:
                        pass
        logger.warning("Could not parse JSON from LLM response.")
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
    # Filter out empty responses before scoring consensus
    non_empty = [r for r in responses if r]
    if not non_empty:
        return 0.0
    counts = Counter(str(r) for r in non_empty)
    return max(counts.values()) / len(non_empty)
