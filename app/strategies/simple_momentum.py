from sqlalchemy import text

from app.database.models import TradeSignal
from app.database.session import SessionLocal


def generate_momentum_signal(market: str) -> TradeSignal | None:
    db = SessionLocal()
    try:
        rows = db.execute(
            text("""
                SELECT price
                FROM price_ticks
                WHERE market = :market
                ORDER BY id DESC
                LIMIT 5
            """),
            {"market": market},
        ).fetchall()

        if len(rows) < 5:
            return None

        latest = float(rows[0][0])
        oldest = float(rows[-1][0])
        change_percent = ((latest - oldest) / oldest) * 100

        if change_percent > 0.15:
            signal = "BUY"
            confidence = min(0.95, 0.60 + abs(change_percent))
            reason = f"Momentum positief: prijs steeg {change_percent:.3f}% over laatste 5 ticks."
        elif change_percent < -0.15:
            signal = "SELL"
            confidence = min(0.95, 0.60 + abs(change_percent))
            reason = f"Momentum negatief: prijs daalde {change_percent:.3f}% over laatste 5 ticks."
        else:
            signal = "HOLD"
            confidence = 0.50
            reason = f"Geen duidelijk momentum: verandering {change_percent:.3f}%."

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
