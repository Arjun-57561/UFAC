# research/llama_api_test.py
"""
Experiment: Using a local Llama model (via Ollama) on the PM-KISAN data.

This script loads the PM-KISAN rules from data/pm_kisan_rules.py and
uses a locally-running Llama model through the Ollama HTTP API to answer
eligibility questions about the scheme.

Requirements:
    1. Install Ollama: https://ollama.com/download
    2. Pull a Llama model:
           ollama pull llama3
    3. Start the Ollama server:
           ollama serve
    4. Install the requests library (usually pre-installed):
           pip install requests python-dotenv

Environment variables (optional):
    OLLAMA_HOST  — Ollama server URL (default: http://localhost:11434)
    OLLAMA_MODEL — Model name to use   (default: llama3)
"""

import os
import json
import sys
import requests

# Allow running from any working directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from dotenv import load_dotenv
from data.pm_kisan_rules import PM_KISAN_RULES
from research.utils import build_prompt, extract_json_from_response

load_dotenv()

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")


def check_ollama_running() -> bool:
    """Return True if the Ollama server is reachable."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        return resp.status_code == 200
    except requests.ConnectionError:
        return False


def run_llama_experiment(user_profile: dict) -> dict:
    print(f"\n{'='*60}")
    print(f"Llama (Ollama) — PM-KISAN Eligibility Check  [model: {OLLAMA_MODEL}]")
    print(f"{'='*60}")
    print(f"User profile: {json.dumps(user_profile, indent=2)}\n")

    if not check_ollama_running():
        print(
            f"⚠  Ollama server is not reachable at {OLLAMA_HOST}.\n"
            "   Start it with:  ollama serve\n"
            "   Then pull a model with:  ollama pull llama3"
        )
        return {}

    prompt = build_prompt(PM_KISAN_RULES, user_profile)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.2},
    }

    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    raw_text = response.json().get("response", "").strip()

    result = extract_json_from_response(raw_text)

    print("Llama response:")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    # Test profiles
    profiles = [
        {
            "name": "Ramesh Kumar",
            "occupation": "farmer",
            "land_owner": True,
            "aadhaar_linked": True,
            "aadhaar_ekyc_done": True,
            "bank_account": True,
            "farmer_status": "small_marginal",
            "income_tax_payer": False,
            "govt_employee": False,
            "pension_above_10k": False,
            "practicing_professional": False,
            "constitutional_post_holder": False,
            "institutional_landholder": False,
        },
        {
            "name": "Suresh Sharma",
            "occupation": "farmer",
            "land_owner": True,
            "income_tax_payer": True,  # Disqualifier
            "govt_employee": False,
        },
        {
            "name": "Priya Devi",
            "occupation": "farmer",
            # Many required fields missing
            "bank_account": True,
        },
    ]

    for profile in profiles:
        run_llama_experiment(profile)
        print()
