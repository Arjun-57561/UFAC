# File: main.py
import asyncio
import json
from core.ufac_engine import run_ufac
from core.llm_utils import init_gemini

async def main():
    # Initialize Gemini API
    init_gemini()
    
    # Test case 1: Minimal input
    print("\n" + "="*60)
    print("TEST 1: Minimal Input (Farmer)")
    print("="*60)
    user_input_1 = {
        "occupation": "farmer"
    }
    response_1 = await run_ufac(user_input_1)
    print(json.dumps(json.loads(response_1.model_dump_json()), indent=2))

    # Test case 2: More complete input
    print("\n" + "="*60)
    print("TEST 2: More Complete Input")
    print("="*60)
    user_input_2 = {
        "occupation": "farmer",
        "land_ownership": "yes",
        "land_size_hectares": 2.5,
        "aadhaar_linked": True,
        "aadhaar_ekyc_done": True,
        "bank_account": True,
        "state": "Punjab",
        "district": "Ludhiana"
    }
    response_2 = await run_ufac(user_input_2)
    print(json.dumps(json.loads(response_2.model_dump_json()), indent=2))

    # Test case 3: Incomplete input
    print("\n" + "="*60)
    print("TEST 3: Incomplete Input")
    print("="*60)
    user_input_3 = {
        "occupation": "farmer",
        "annual_income": 150000
    }
    response_3 = await run_ufac(user_input_3)
    print(json.dumps(json.loads(response_3.model_dump_json()), indent=2))

    # Test case 4: Disqualifier case
    print("\n" + "="*60)
    print("TEST 4: Disqualifier Case")
    print("="*60)
    user_input_4 = {
        "occupation": "farmer",
        "land_ownership": "yes",
        "income_tax_payer": True,
        "govt_employee": False
    }
    response_4 = await run_ufac(user_input_4)
    print(json.dumps(json.loads(response_4.model_dump_json()), indent=2))

if __name__ == "__main__":
    asyncio.run(main())

