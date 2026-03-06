from core.ufac_engine import run_ufac

def main():
    # Minimal test input
    user_input = {
        "occupation": "farmer"
    }

    response = run_ufac(user_input)

    # Pretty print output
    print("\n--- UFAC OUTPUT ---")
    print(response.model_dump_json(indent=2))

if __name__ == "__main__":
    main()
