# File: main.py
import asyncio
import json
import time
from core.ufac_engine import run_ufac
from core.llm_utils import init_gemini


async def run_test(name: str, user_input: dict):
    print(f"\n{'='*60}\n{name}\n{'='*60}")
    try:
        start = time.perf_counter()
        response = await run_ufac(user_input)
        elapsed = time.perf_counter() - start
        print(json.dumps(json.loads(response.model_dump_json()), indent=2))
        print(f"⏱  Completed in {elapsed:.2f}s")
    except Exception as e:
        print(f"❌ Test failed: {e}")


async def main():
    init_gemini()

    await run_test("TEST 1: Minimal Input (Farmer)", {
        "occupation": "farmer"
    })

    await run_test("TEST 2: Complete Input", {
        "occupation": "farmer",
        "land_ownership": "yes",
        "aadhaar_linked": True,
        "aadhaar_ekyc_done": True,
        "bank_account": True,
        "state": "Punjab",
        "district": "Ludhiana"
    })

    await run_test("TEST 3: Incomplete Input", {
        "occupation": "farmer",
        "annual_income": 150000
    })

    await run_test("TEST 4: Disqualifier Case", {
        "occupation": "farmer",
        "land_ownership": "yes",
        "income_tax_payer": True,
        "govt_employee": False
    })


if __name__ == "__main__":
    asyncio.run(main())
