from sqlalchemy import text
from app.database.session import SessionLocal


def get_position_summary(market: str) -> dict:
    """
    Return position summary for a market based on paper trades.
    """

    db = SessionLocal()

    try:
        buys = db.execute(
            text("""
                SELECT COUNT(*), COALESCE(SUM(amount_eur), 0)
                FROM paper_trades
                WHERE market = :market AND side = 'BUY'
            """),
            {"market": market},
        ).first()

        sells = db.execute(
            text("""
                SELECT COUNT(*), COALESCE(SUM(amount_eur), 0)
                FROM paper_trades
                WHERE market = :market AND side = 'SELL'
            """),
            {"market": market},
        ).first()

        buy_count = buys[0]
        total_bought_eur = float(buys[1])

        sell_count = sells[0]
        total_sold_eur = float(sells[1])

        open_position_count = max(0, buy_count - sell_count)
        exposure_eur = max(0, total_bought_eur - total_sold_eur)

        return {
            "market": market,
            "buy_count": buy_count,
            "sell_count": sell_count,
            "open_position_count": open_position_count,
            "exposure_eur": exposure_eur,
            "has_open_position": open_position_count > 0,
        }

    finally:
        db.close()
