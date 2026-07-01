from sqlalchemy import text


def get_latest_trades(db, limit: int = 5) -> list[dict]:
    rows = db.execute(text("""
        SELECT id, market, side, amount_eur, price, created_at
        FROM paper_trades
        ORDER BY id
    """)).fetchall()

    trades = []
    open_buy_price = None
    open_amount_eur = None

    for row in rows:
        trade_id, market, side, amount_eur, price, created_at = row

        pnl_eur = None

        if side == "BUY":
            open_buy_price = float(price)
            open_amount_eur = float(amount_eur)

        elif side == "SELL" and open_buy_price and open_amount_eur:
            pnl_eur = (
                (float(price) - open_buy_price) / open_buy_price
            ) * open_amount_eur
            open_buy_price = None
            open_amount_eur = None

        trades.append(
            {
                "id": trade_id,
                "market": market,
                "side": side,
                "amount_eur": float(amount_eur),
                "price": float(price),
                "created_at": created_at,
                "pnl_eur": pnl_eur,
            }
        )

    return list(reversed(trades))[:limit]
