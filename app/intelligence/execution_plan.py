def build_execution_plan(
    market: str,
    decision: dict,
    max_position_eur: float,
) -> dict:
    """
    Build an execution plan from a decision.
    """

    if decision["blocked"]:
        return {
            "market": market,
            "action": "HOLD",
            "amount_eur": 0,
            "reason": decision["reason"],
        }

    if decision["action"] == "BUY":
        return {
            "market": market,
            "action": "BUY",
            "amount_eur": max_position_eur,
            "reason": decision["reason"],
        }

    if decision["action"] == "SELL":
        return {
            "market": market,
            "action": "SELL",
            "amount_eur": 0,
            "reason": decision["reason"],
        }

    return {
        "market": market,
        "action": "HOLD",
        "amount_eur": 0,
        "reason": decision["reason"],
    }
