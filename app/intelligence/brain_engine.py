def calculate_brain_score(technical: dict, sentiment: dict) -> dict:
    """
    Calculate Atlas Brain score from technical and sentiment inputs.
    """

    score = 50
    score_breakdown = []

    technical_bias = technical.get("bias", "neutral")
    consensus = technical.get("consensus", 50)
    sentiment_value = sentiment.get("value", 50)

    if technical_bias == "bullish":
        score += 20
        score_breakdown.append("+20 Technical bias is bullish.")

    elif technical_bias == "bearish":
        score -= 20
        score_breakdown.append("-20 Technical bias is bearish.")

    else:
        score_breakdown.append("+0 Technical bias is neutral.")

    if consensus >= 75:
        score += 15
        score_breakdown.append("+15 Technical consensus is strong.")
    elif consensus <= 50:
        score -= 5
        score_breakdown.append("-5 Technical consensus is weak.")

    if sentiment_value < 40:
        score += 10
        score_breakdown.append("+10 Market sentiment is fearful.")
    elif sentiment_value > 60:
        score -= 10
        score_breakdown.append("-10 Market sentiment is greedy.")
    else:
        score_breakdown.append("+0 Market sentiment is neutral.")

    score = max(0, min(100, score))

    return {
        "score": score,
        "score_breakdown": score_breakdown,
    }
