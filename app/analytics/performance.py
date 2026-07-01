from sqlalchemy import text


def calculate_performance(db, market: str = "BTC-EUR") -> dict:
    performance = db.execute(
        text("""
        WITH ordered_trades AS (
            SELECT
                id,
                side,
                amount_eur,
                price,
                ROW_NUMBER() OVER (ORDER BY id) AS rn
            FROM paper_trades
            WHERE market = :market
        ),
        matched_trades AS (
            SELECT
                ((sell.price - buy.price) / buy.price) * buy.amount_eur AS pnl_eur
            FROM ordered_trades buy
            JOIN ordered_trades sell
                ON sell.rn = buy.rn + 1
            WHERE buy.side = 'BUY'
              AND sell.side = 'SELL'
        )
        SELECT
            COUNT(*) AS closed_trades,
            COALESCE(SUM(pnl_eur), 0) AS total_pnl_eur,
            COALESCE(AVG(pnl_eur), 0) AS avg_pnl_eur,
            COALESCE(SUM(CASE WHEN pnl_eur > 0 THEN 1 ELSE 0 END), 0) AS winning_trades
        FROM matched_trades
    """),
        {"market": market},
    ).fetchone()

    closed_trades = performance[0]
    total_pnl_eur = float(performance[1])
    avg_pnl_eur = float(performance[2])
    winning_trades = performance[3]

    if closed_trades > 0:
        winrate = (winning_trades / closed_trades) * 100
    else:
        winrate = 0.0

    return {
        "closed_trades": closed_trades,
        "total_pnl_eur": total_pnl_eur,
        "avg_pnl_eur": avg_pnl_eur,
        "winrate": winrate,
    }
