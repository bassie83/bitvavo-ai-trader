from app.intelligence.brain_engine import calculate_brain_score


def analyze_brain(technical: dict, sentiment: dict) -> dict:
    """
    Combine technical and sentiment intelligence.
    """

    technical_bias = technical.get("bias", "neutral")
    sentiment_value = sentiment.get("value", 50)
    brain = calculate_brain_score(technical, sentiment)
    brain_score = brain["score"]
    brain_breakdown = brain["score_breakdown"]

    if technical_bias == "bullish" and sentiment_value < 40:
        return {
            "bias": "cautious_bullish",
            "action": "BUY",
            "message": "Technicals are bullish while market sentiment remains fearful.",
            "brain_score": brain_score,
            "score_breakdown": brain_breakdown,
        }

    if technical_bias == "bearish" and sentiment_value > 60:
        return {
            "bias": "cautious_bearish",
            "action": "SELL",
            "message": "Technicals are bearish while market sentiment remains greedy.",
            "brain_score": brain_score,
            "score_breakdown": brain_breakdown,
        }

    return {
        "bias": technical_bias,
        "action": "HOLD",
        "message": "Technical and sentiment are aligned.",
        "brain_score": brain_score,
        "score_breakdown": brain_breakdown,
    }
