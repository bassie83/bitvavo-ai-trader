from app.intelligence.scoring import score_sentiment
from app.intelligence.scoring import (
    score_sentiment,
    score_technical_bias,
)


def calculate_brain_score(technical: dict, sentiment: dict) -> dict:
    """
    Calculate Atlas Brain score from technical and sentiment inputs.
    """

    score = 50
    score_breakdown = []

    technical_bias = technical.get("bias", "neutral")
    consensus = technical.get("consensus", 50)
    sentiment_value = sentiment.get("value", 50)

    technical_score, technical_reason = score_technical_bias(technical_bias)
    score += technical_score
    score_breakdown.append(f"{technical_score:+d} {technical_reason}")

    consensus_score, consensus_reason = score_consensus(consensus)
    score += consensus_score
    score_breakdown.append(f"{consensus_score:+d} {consensus_reason}")

    sentiment_score, sentiment_reason = score_sentiment(sentiment_value)
    score += sentiment_score
    score_breakdown.append(f"{sentiment_score:+d} {sentiment_reason}")

    score = max(0, min(100, score))

    return {
        "score": score,
        "score_breakdown": score_breakdown,
    }


def score_consensus(consensus: int) -> tuple[int, str]:
    """
    Score technical consensus between -5 and +15.
    """

    if consensus >= 75:
        return 15, "Technical consensus is strong."

    if consensus <= 50:
        return -5, "Technical consensus is weak."

    return 0, "Technical consensus is neutral."
