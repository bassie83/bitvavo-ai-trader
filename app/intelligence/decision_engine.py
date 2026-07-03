def make_decision(brain_score: int) -> dict:
    """
    Convert a Brain Score into a trading decision.
    """

    if brain_score >= 80:
        return {
            "action": "BUY",
            "confidence": "HIGH",
        }

    if brain_score <= 20:
        return {
            "action": "SELL",
            "confidence": "HIGH",
        }

    return {
        "action": "HOLD",
        "confidence": "MEDIUM",
    }
