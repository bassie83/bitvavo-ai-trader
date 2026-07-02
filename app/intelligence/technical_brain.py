def analyze_technical_brain(rsi: dict, macd: dict) -> dict:
    """
    Combine RSI and MACD intelligence into one weighted technical assessment.
    """

    rsi_bias = rsi.get("bias", "neutral")
    macd_bias = macd.get("bias", "neutral")

    rsi_weight = rsi.get("weight", 0)
    macd_weight = macd.get("weight", 0)

    if rsi_bias == macd_bias:
        return {
            "bias": rsi_bias,
            "agreement": True,
            "consensus": 100,
            "weighted_score": rsi_weight + macd_weight,
            "message": f"RSI and MACD are both {rsi_bias}.",
        }

    return {
        "bias": "neutral",
        "agreement": False,
        "consensus": 50,
        "weighted_score": 0,
        "message": "RSI and MACD do not agree.",
    }
