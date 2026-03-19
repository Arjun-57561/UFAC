# File: core/llm_utils.py
import os
import asyncio
import json
import logging
from typing import List, Dict, Any

import google.generativeai as genai

logger = logging.getLogger(__name__)

GEMINI_API_KEY: str | None = None  # Initialized via lifespan

def init_gemini():
    global GEMINI_API_KEY
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    GEMINI_API_KEY = key
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API initialized successfully.")

async def _single_llm_call(prompt: str, temperature: float, run_index: int) -> Dict[str, Any]:
    """Single async Gemini call with timeout and retry."""
    model = genai.GenerativeModel("gemini-1.5-flash")
    loop = asyncio.get_event_loop()

    def _call():
        return model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=500,
                top_p=0.95,
            ),
        )

    for attempt in range(2):  # 1 retry on failure
        try:
            response = await asyncio.wait_for(
                loop.run_in_executor(None, _call),
                timeout=15.0,
            )
            return extract_json_from_response(response.text.strip())
        except asyncio.TimeoutError:
            logger.warning(f"Run {run_index+1} attempt {attempt+1} timed out.")
        except Exception as e:
            logger.error(f"Run {run_index+1} attempt {attempt+1} error: {e}")
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
    counts = Counter(str(r) for r in responses)
    return max(counts.values()) / len(responses)