def analyze_rsi(rsi: float) -> dict:
    """
    Analyze RSI value and return RSI intelligence.

    RSI interpretation:
    - Below 30: oversold, bullish reversal potential
    - Above 70: overbought, bearish reversal risk
    - Between 30 and 70: neutral
    """

    if rsi < 30:
        return {
            "indicator": "RSI",
            "value": rsi,
            "zone": "oversold",
            "bias": "bullish",
            "message": "RSI is oversold. This may indicate bullish reversal potential.",
        }

    if rsi > 70:
        return {
            "indicator": "RSI",
            "value": rsi,
            "zone": "overbought",
            "bias": "bearish",
            "message": "RSI is overbought. This may indicate bearish reversal risk.",
        }

    return {
        "indicator": "RSI",
        "value": rsi,
        "zone": "neutral",
        "bias": "neutral",
        "message": "RSI is neutral. No strong RSI-based signal detected.",
    }
