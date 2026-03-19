# research/gemini_api_test.py
"""
Experiment: Using Google Gemini API on the PM-KISAN data.

This script loads the PM-KISAN rules from data/pm_kisan_rules.py and
uses the Gemini API (google-generativeai) to answer eligibility questions
about the scheme.

Requirements:
    pip install google-generativeai python-dotenv

Environment variables:
    GEMINI_API_KEY  — your Google AI Studio API key
                      (https://aistudio.google.com/app/apikey)
"""

import os
import json
import sys

# Allow running from any working directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import google.generativeai as genai
from dotenv import load_dotenv
from data.pm_kisan_rules import PM_KISAN_RULES
from research.utils import build_prompt, extract_json_from_response

load_dotenv()


def init_gemini() -> genai.GenerativeModel:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable is not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def run_gemini_experiment(user_profile: dict) -> dict:
    model = init_gemini()
    prompt = build_prompt(PM_KISAN_RULES, user_profile)

    print(f"\n{'='*60}")
    print("Gemini API — PM-KISAN Eligibility Check")
    print(f"{'='*60}")
    print(f"User profile: {json.dumps(user_profile, indent=2)}\n")

    response = model.generate_content(prompt)
    result = extract_json_from_response(response.text.strip())

    print("Gemini response:")
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
        run_gemini_experiment(profile)
        print()
