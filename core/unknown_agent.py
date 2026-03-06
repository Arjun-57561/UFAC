def detect_unknowns(user_data, rules):
    unknowns = []

    for field in rules["required_fields"]:
        if field not in user_data:
            unknowns.append(f"Missing information: {field}")

    return unknowns
