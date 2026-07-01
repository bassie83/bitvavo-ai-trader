from sqlalchemy import text


def calculate_portfolio(db, settings, market: str = "BTC-EUR") -> dict:
    buys_total = db.execute(
        text("""
        SELECT COALESCE(SUM(amount_eur), 0)
        FROM paper_trades
        WHERE side = 'BUY'
          AND market = :market
    """),
        {"market": market},
    ).scalar()

    sells_total = db.execute(
        text("""
        SELECT COALESCE(SUM(amount_eur), 0)
        FROM paper_trades
        WHERE side = 'SELL'
          AND market = :market
    """),
        {"market": market},
    ).scalar()

    buy_count = db.execute(
        text("""
        SELECT COUNT(*)
        FROM paper_trades
        WHERE side = 'BUY'
          AND market = :market
    """),
        {"market": market},
    ).scalar()

    sell_count = db.execute(
        text("""
        SELECT COUNT(*)
        FROM paper_trades
        WHERE side = 'SELL'
          AND market = :market
    """),
        {"market": market},
    ).scalar()

    cash_balance = (
        settings.paper_start_balance_eur - float(buys_total) + float(sells_total)
    )

    open_position_value = 0.0
    if buy_count > sell_count:
        open_position_value = settings.max_position_eur

    portfolio_value = cash_balance + open_position_value
    portfolio_pnl = portfolio_value - settings.paper_start_balance_eur
    portfolio_growth_percent = (portfolio_pnl / settings.paper_start_balance_eur) * 100

    return {
        "cash_balance": cash_balance,
        "open_position_value": open_position_value,
        "portfolio_value": portfolio_value,
        "portfolio_pnl": portfolio_pnl,
        "portfolio_growth_percent": portfolio_growth_percent,
        "has_open_position": buy_count > sell_count,
    }
