def detect_assumptions(user_data):
    assumptions = []

    if "land_owner" not in user_data:
        assumptions.append("User owns agricultural land")

    if "aadhaar_linked" not in user_data:
        assumptions.append("Aadhaar is linked to bank account")

    return assumptions
