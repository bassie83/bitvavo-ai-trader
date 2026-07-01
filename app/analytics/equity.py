from sqlalchemy import text


def calculate_equity_points(db, settings, market: str = "BTC-EUR") -> list[dict]:
    rows = db.execute(
        text("""
        SELECT id, created_at, side, amount_eur, price
        FROM paper_trades
        WHERE market = :market
        ORDER BY id
    """),
        {"market": market},
    ).fetchall()

    equity = settings.paper_start_balance_eur
    open_buy_price = None
    open_amount_eur = None
    points = []

    for row in rows:
        trade_id, created_at, side, amount_eur, price = row

        if side == "BUY":
            open_buy_price = float(price)
            open_amount_eur = float(amount_eur)

        elif side == "SELL" and open_buy_price and open_amount_eur:
            pnl = ((float(price) - open_buy_price) / open_buy_price) * open_amount_eur
            equity += pnl

            points.append(
                {
                    "trade_id": trade_id,
                    "created_at": str(created_at),
                    "equity": equity,
                    "pnl": pnl,
                }
            )

            open_buy_price = None
            open_amount_eur = None

    return points
