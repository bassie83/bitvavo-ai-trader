def analyze_brain(technical: dict, sentiment: dict) -> dict:
    """
    Combine technical and sentiment intelligence.
    """

    technical_bias = technical.get("bias", "neutral")
    sentiment_value = sentiment.get("value", 50)

    if technical_bias == "bullish" and sentiment_value < 40:
        return {
            "bias": "cautious_bullish",
            "action": "BUY",
            "message": "Technicals are bullish while market sentiment remains fearful.",
            "reasons": [
                "Technical indicators are bullish.",
                "Market sentiment is fearful.",
                "Fearful sentiment may create a cautious buying opportunity.",
            ],
        }

    if technical_bias == "bearish" and sentiment_value > 60:
        return {
            "bias": "cautious_bearish",
            "action": "SELL",
            "message": "Technicals are bearish while market sentiment remains greedy.",
            "reasons": [
                "Technical indicators are bearish.",
                "Market sentiment is greedy.",
                "Greedy sentiment may increase downside risk.",
            ],
        }

    return {
        "bias": technical_bias,
        "action": "HOLD",
        "message": "Technical and sentiment are aligned.",
        "reasons": [
            "No strong conflict detected between technicals and sentiment.",
            "Atlas keeps a neutral risk posture.",
        ],
    }
