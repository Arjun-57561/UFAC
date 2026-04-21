# research/utils.py
"""
Shared utilities for the research API experiment scripts.
"""

import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def build_prompt(scheme: dict, user_profile: dict) -> str:
    """Build a standardised eligibility-check prompt for any LLM."""
    return f"""
You are an expert on Indian government welfare schemes.

Below are the rules for the {scheme['name']} scheme:
{json.dumps(scheme, indent=2)}

A farmer has provided the following profile:
{json.dumps(user_profile, indent=2)}

Based on the scheme rules, answer the following:
1. Is the farmer likely ELIGIBLE or INELIGIBLE for {scheme['name']}?
2. List any disqualifiers that apply.
3. List any required fields that are missing from the profile.
4. Provide a brief explanation (2-3 sentences).

Respond ONLY in JSON with keys: eligible (bool), disqualifiers (list), missing_fields (list), explanation (str).
"""


def extract_json_from_response(raw_text: str) -> Dict[str, Any]:
    """Parse a JSON object from a raw LLM response string."""
    for marker in ["```json", "```"]:
        if marker in raw_text:
            start = raw_text.find(marker) + len(marker)
            end = raw_text.find("```", start)
            if end > start:
                try:
                    return json.loads(raw_text[start:end].strip())
                except json.JSONDecodeError:
                    pass
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        logger.warning("Could not parse JSON from LLM response.")
        return {"raw_response": raw_text}
