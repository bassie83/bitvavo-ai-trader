from app.strategies.indicators import calculate_trend_score
from app.intelligence.rsi import analyze_rsi


def get_technical_intelligence(market: str = "BTC-EUR") -> dict:
    analysis = calculate_trend_score(market)
    rsi_value = analysis.get("rsi")

    return {
        "ready": analysis.get("ready", False),
        "score": analysis.get("score", 0),
        "advice": analysis.get("advice", "UNKNOWN"),
        "rsi": rsi_value,
        "rsi_analysis": analyze_rsi(rsi_value) if rsi_value is not None else None,
        "macd": analysis.get("macd", {}),
        "reason": analysis.get("reason", ""),
    }
