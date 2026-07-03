def make_decision(
    brain_score: int,
    has_open_position: bool = False,
    risk_allowed: bool = True,
) -> dict:
    """
    Convert a Brain Score and trading context into a trading decision.
    """

    if not risk_allowed:
        return {
            "action": "HOLD",
            "confidence": "LOW",
            "reason": "Risk Manager blocks trading.",
            "blocked": True,
        }

    if brain_score >= 80 and not has_open_position:
        return {
            "action": "BUY",
            "confidence": "HIGH",
            "reason": "Brain Score is high and no position is open.",
            "blocked": False,
        }

    if brain_score <= 20 and has_open_position:
        return {
            "action": "SELL",
            "confidence": "HIGH",
            "reason": "Brain Score is low and a position is open.",
            "blocked": False,
        }

    return {
        "action": "HOLD",
        "confidence": "MEDIUM",
        "reason": "No context-aware trade condition is met.",
        "blocked": False,
    }
