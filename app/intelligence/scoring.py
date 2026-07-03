def score_rsi(rsi: float) -> tuple[int, str]:
    """
    Score RSI between -20 and +20.
    """

    if rsi < 30:
        return 20, "RSI is oversold."

    if rsi > 70:
        return -20, "RSI is overbought."

    return 0, "RSI is neutral."


def score_sentiment(value: int) -> tuple[int, str]:
    """
    Score Fear & Greed between -10 and +10.
    """

    if value < 30:
        return 10, "Market sentiment is fearful."

    if value > 70:
        return -10, "Market sentiment is greedy."

    return 0, "Market sentiment is neutral."


def score_technical_bias(bias: str) -> tuple[int, str]:
    """
    Score technical bias between -20 and +20.
    """

    if bias == "bullish":
        return 20, "Technical bias is bullish."

    if bias == "bearish":
        return -20, "Technical bias is bearish."

    return 0, "Technical bias is neutral."
