def analyze_technical_brain(rsi: dict, macd: dict) -> dict:
    """
    Combine RSI and MACD intelligence into one technical assessment.
    """

    if rsi["bias"] == macd["bias"]:
        return {
            "bias": rsi["bias"],
            "agreement": True,
            "consensus": 100,
            "message": f"RSI and MACD are both {rsi['bias']}.",
        }

    return {
        "bias": "neutral",
        "agreement": False,
        "consensus": 50,
        "message": "RSI and MACD do not agree.",
    }
