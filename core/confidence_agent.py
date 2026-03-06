def calculate_confidence(known, unknowns):
    confidence = 100
    confidence -= len(unknowns) * 15
    confidence += len(known) * 10

    return max(0, min(confidence, 100))
