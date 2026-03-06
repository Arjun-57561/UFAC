def generate_next_steps(unknowns):
    if not unknowns:
        return ["You can proceed with application"]

    return [
        "Verify missing information before applying",
        "Visit CSC or government office for assistance"
    ]
