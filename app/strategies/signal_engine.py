from app.database.models import TradeSignal
from app.database.session import SessionLocal
from app.strategies.indicators import calculate_trend_score


def generate_combined_signal(market: str) -> TradeSignal:
    analysis = calculate_trend_score(market)

    macd = analysis.get("macd")
    macd_signal = macd.get("signal") if macd else None

    if (
        not analysis.get("ready")
        or analysis.get("rsi") is None
        or macd_signal in (None, "n/a")
    ):
        signal = "HOLD"
        confidence = 0.0
        reason = analysis.get("reason", "Indicatoren nog niet volledig beschikbaar.")
    else:
        score = analysis["score"]

        if score >= 75:
            signal = "BUY"
        elif score <= 25:
            signal = "SELL"
        else:
            signal = "HOLD"

        if signal == "BUY":
            confidence = score / 100
        elif signal == "SELL":
            confidence = (100 - score) / 100
        else:
            confidence = 1 - abs(score - 50) / 50

        reason = (
            f"Score {score}/100. "
            f"Advies: {analysis['advice']}. "
            f"RSI: {analysis.get('rsi')}. "
            f"MACD: {macd_signal}."
        )

    db = SessionLocal()
    try:
        trade_signal = TradeSignal(
            market=market,
            signal=signal,
            confidence=confidence,
            reason=reason,
        )
        db.add(trade_signal)
        db.commit()
        db.refresh(trade_signal)
        return trade_signal
    finally:
        db.close()
