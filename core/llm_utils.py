# File: core/llm_utils.py
import os
import google.generativeai as genai
from typing import List, Dict, Any
import json

# Set your Gemini API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")
genai.configure(api_key=GEMINI_API_KEY)

def run_llm_council(prompt: str, num_runs: int = 3) -> List[Dict[str, Any]]:
    """Run the Gemini LLM multiple times and collect responses."""
    responses = []
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    for i in range(num_runs):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7 + (i * 0.1),  # Vary temperature for diversity
                    max_output_tokens=500,
                    top_p=0.95,
                )
            )
            content = response.text.strip()
            # Extract JSON from response
            parsed = extract_json_from_response(content)
            responses.append(parsed)
        except Exception as e:
            print(f"Error in Gemini call (run {i+1}): {e}")
            responses.append({})  # Empty on error
    return responses

def extract_json_from_response(text: str) -> Dict[str, Any]:
    """Extract JSON from LLM response, handling markdown code blocks."""
    try:
        # Try direct JSON parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        # Try extracting from markdown code block
        if "```json" in text:
            start = text.find("```json") + 7
            end = text.find("```", start)
            if end > start:
                return json.loads(text[start:end].strip())
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            if end > start:
                return json.loads(text[start:end].strip())
        # If all else fails, return empty dict
        return {}

def aggregate_list_responses(responses: List[List[str]], threshold: float = 0.5) -> List[str]:
    """Aggregate list responses by majority vote."""
    if not responses:
        return []
    all_items = {}
    total_runs = len(responses)
    for resp in responses:
        for item in resp:
            all_items[item] = all_items.get(item, 0) + 1
    aggregated = [item for item, count in all_items.items() if count / total_runs >= threshold]
    return aggregated

def aggregate_score_responses(responses: List[float]) -> float:
    """Average the scores."""
    if not responses:
        return 0.0
    return sum(responses) / len(responses)

def calculate_consensus(responses: List[Any]) -> float:
    """Simple consensus score: fraction of identical responses."""
    if not responses:
        return 0.0
    from collections import Counter
    counts = Counter(str(r) for r in responses)
    max_count = max(counts.values())
    return max_count / len(responses)