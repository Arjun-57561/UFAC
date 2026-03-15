# File: main.py
from core.ufac_engine import run_ufac
import json

def main():
    # Test case 1: Minimal input
    print("\n" + "="*60)
    print("TEST 1: Minimal Input (Farmer)")
    print("="*60)
    user_input_1 = {
        "occupation": "farmer"
    }
    response_1 = run_ufac(user_input_1)
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
        "bank_account": True,
        "state": "Punjab",
        "district": "Ludhiana"
    }
    response_2 = run_ufac(user_input_2)
    print(json.dumps(json.loads(response_2.model_dump_json()), indent=2))

    # Test case 3: Incomplete input
    print("\n" + "="*60)
    print("TEST 3: Incomplete Input")
    print("="*60)
    user_input_3 = {
        "occupation": "farmer",
        "annual_income": 150000
    }
    response_3 = run_ufac(user_input_3)
    print(json.dumps(json.loads(response_3.model_dump_json()), indent=2))

if __name__ == "__main__":
    main()

