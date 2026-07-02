from app.strategies.indicators import calculate_trend_score


def get_technical_intelligence(market: str = "BTC-EUR") -> dict:
    analysis = calculate_trend_score(market)

    return {
        "ready": analysis.get("ready", False),
        "score": analysis.get("score", 0),
        "advice": analysis.get("advice", "UNKNOWN"),
        "rsi": analysis.get("rsi"),
        "macd": analysis.get("macd", {}),
        "reason": analysis.get("reason", ""),
    }
