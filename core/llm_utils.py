import os
import openai
from typing import List, Dict, Any
import json

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def run_llm_council(prompt: str, num_runs: int = 3) -> List[Dict[str, Any]]:
    """Run the LLM multiple times and collect responses."""
    responses = []
    for _ in range(num_runs):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7  # Some randomness for diversity
            )
            content = response.choices[0].message.content.strip()
            # Assume the response is JSON
            parsed = json.loads(content)
            responses.append(parsed)
        except Exception as e:
            print(f"Error in LLM call: {e}")
            responses.append({})  # Empty on error
    return responses

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