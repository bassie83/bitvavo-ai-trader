from app.intelligence.brain_engine import calculate_brain_score
from app.intelligence.decision_engine import make_decision


def analyze_brain(
    technical: dict,
    sentiment: dict,
    has_open_position: bool = False,
    risk_allowed: bool = True,
) -> dict:
    """
    Combine technical and sentiment intelligence.
    """

    technical_bias = technical.get("bias", "neutral")
    sentiment_value = sentiment.get("value", 50)
    brain = calculate_brain_score(technical, sentiment)
    brain_score = brain["score"]
    brain_breakdown = brain["score_breakdown"]

    decision = make_decision(
        brain_score=brain_score,
        has_open_position=has_open_position,
        risk_allowed=risk_allowed,
    )

    if technical_bias == "bullish" and sentiment_value < 40:
        return {
            "bias": "cautious_bullish",
            "action": decision["action"],
            "confidence": decision["confidence"],
            "message": "Technicals are bullish while market sentiment remains fearful.",
            "brain_score": brain_score,
            "score_breakdown": brain_breakdown,
            "blocked": decision["blocked"],
            "decision_reason": decision["reason"],
        }

    if technical_bias == "bearish" and sentiment_value > 60:
        return {
            "bias": "cautious_bearish",
            "action": decision["action"],
            "confidence": decision["confidence"],
            "message": "Technicals are bearish while market sentiment remains greedy.",
            "brain_score": brain_score,
            "score_breakdown": brain_breakdown,
            "blocked": decision["blocked"],
            "decision_reason": decision["reason"],
        }

    return {
        "bias": technical_bias,
        "action": decision["action"],
        "confidence": decision["confidence"],
        "message": "Technical and sentiment are aligned.",
        "brain_score": brain_score,
        "score_breakdown": brain_breakdown,
        "blocked": decision["blocked"],
        "decision_reason": decision["reason"],
    }
