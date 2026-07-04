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
            "message": "Technicals are bullish while market sentiment remains fearful.",
            "brain_score": brain_score,
            "score_breakdown": brain_breakdown,
            "decision": decision,
        }

    if technical_bias == "bearish" and sentiment_value > 60:
        return {
            "bias": "cautious_bearish",
            "message": "Technicals are bearish while market sentiment remains greedy.",
            "brain_score": brain_score,
            "score_breakdown": brain_breakdown,
            "decision": decision,
        }

    return {
        "bias": technical_bias,
        "message": "Technical and sentiment are aligned.",
        "brain_score": brain_score,
        "score_breakdown": brain_breakdown,
        "decision": decision,
    }


def analyze_market_context(context) -> dict:
    """
    Analyze a complete MarketContext.

    Compatibility wrapper around analyze_brain().
    """

    brain = analyze_brain(
        technical=context.technical["brain"],
        sentiment=context.sentiment,
        has_open_position=context.portfolio["has_open_position"],
        risk_allowed=context.risk["allowed"],
    )

    news = context.news

    if news:
        brain["news"] = {
            "summary": news.summary,
            "sentiment": news.sentiment,
            "impact": news.impact,
            "confidence": news.confidence,
            "affected_assets": news.affected_assets,
            "reasoning": news.reasoning,
        }

        brain["score_breakdown"].append(f"+0 News sentiment is {news.sentiment}.")

    return brain
