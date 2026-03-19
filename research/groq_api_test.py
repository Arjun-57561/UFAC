# research/groq_api_test.py
"""
Experiment: Using Groq API on the PM-KISAN data.

This script loads the PM-KISAN rules from data/pm_kisan_rules.py and
uses the Groq API (groq Python SDK) to answer eligibility questions
about the scheme.

Requirements:
    pip install groq python-dotenv

Environment variables:
    GROQ_API_KEY  — your Groq API key (https://console.groq.com/)
"""

import os
import json
import sys

# Allow running from any working directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from groq import Groq
from dotenv import load_dotenv
from data.pm_kisan_rules import PM_KISAN_RULES
from research.utils import build_prompt, extract_json_from_response

load_dotenv()

MODEL_NAME = "llama-3.3-70b-versatile"


def init_groq() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")
    return Groq(api_key=api_key)


def run_groq_experiment(client: Groq, user_profile: dict) -> dict:
    prompt = build_prompt(PM_KISAN_RULES, user_profile)

    print(f"\n{'='*60}")
    print("Groq API — PM-KISAN Eligibility Check")
    print(f"{'='*60}")
    print(f"User profile: {json.dumps(user_profile, indent=2)}\n")

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=512,
    )
    result = extract_json_from_response(response.choices[0].message.content.strip())

    print("Groq response:")
    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    groq_client = init_groq()

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
        run_groq_experiment(groq_client, profile)
        print()
