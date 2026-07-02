def analyze_technical_brain(rsi: dict, macd: dict) -> dict:
    """
    Combine RSI and MACD intelligence into one technical assessment.
    """

    if rsi["bias"] == macd["bias"]:
        return {
            "bias": rsi["bias"],
            "agreement": True,
            "message": f"RSI and MACD are both {rsi['bias']}.",
        }

    return {
        "bias": "neutral",
        "agreement": False,
        "message": "RSI and MACD do not agree.",
    }
