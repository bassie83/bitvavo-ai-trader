def analyze_macd(macd: dict) -> dict:
    """
    Analyze MACD momentum.
    """

    histogram = macd.get("histogram", 0)

    if histogram > 0:
        return {
            "indicator": "MACD",
            "bias": "bullish",
            "message": "MACD shows bullish momentum.",
            "weight": 0.35,
        }

    if histogram < 0:
        return {
            "indicator": "MACD",
            "bias": "bearish",
            "message": "MACD shows bearish momentum.",
            "weight": 0.35,
        }

    return {
        "indicator": "MACD",
        "bias": "neutral",
        "message": "MACD momentum is neutral.",
        "weight": 0.35,
    }
