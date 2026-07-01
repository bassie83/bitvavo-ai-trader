from sqlalchemy import text


def get_latest_trades(db, limit: int = 5) -> list:
    return db.execute(
        text("""
        SELECT id, market, side, amount_eur, price, created_at
        FROM paper_trades
        ORDER BY id DESC
        LIMIT :limit
    """),
        {"limit": limit},
    ).fetchall()
