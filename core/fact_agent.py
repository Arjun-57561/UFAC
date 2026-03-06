# UFAC/core/fact_agent.py


def extract_known_facts(user_data):
    facts = []

    if "farmer" in user_data.get("occupation", "").lower():
        facts.append("User identifies as a farmer")

    return facts
