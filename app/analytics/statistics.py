from sqlalchemy import text


def calculate_statistics(db, market: str = "BTC-EUR") -> dict:
    rows = db.execute(
        text("""
        SELECT id, side, amount_eur, price
        FROM paper_trades
        WHERE market = :market
        ORDER BY id
    """),
        {"market": market},
    ).fetchall()

    open_buy_price = None
    open_amount_eur = None
    pnls = []

    for row in rows:
        trade_id, side, amount_eur, price = row

        if side == "BUY":
            open_buy_price = float(price)
            open_amount_eur = float(amount_eur)

        elif side == "SELL" and open_buy_price and open_amount_eur:
            pnl = ((float(price) - open_buy_price) / open_buy_price) * open_amount_eur
            pnls.append(pnl)

            open_buy_price = None
            open_amount_eur = None

    winners = [pnl for pnl in pnls if pnl > 0]
    losers = [pnl for pnl in pnls if pnl < 0]

    best_trade = max(pnls) if pnls else 0.0
    worst_trade = min(pnls) if pnls else 0.0

    avg_winner = sum(winners) / len(winners) if winners else 0.0
    avg_loser = sum(losers) / len(losers) if losers else 0.0

    gross_profit = sum(winners)
    gross_loss = abs(sum(losers))

    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0.0

    return {
        "winning_trades": len(winners),
        "losing_trades": len(losers),
        "best_trade": best_trade,
        "worst_trade": worst_trade,
        "avg_winner": avg_winner,
        "avg_loser": avg_loser,
        "profit_factor": profit_factor,
    }
