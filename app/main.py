from pathlib import Path
from app.trading_loop import trading_loop
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.strategies.signal_engine import generate_combined_signal
from app.strategies.indicators import calculate_trend_score
from app.telegram.hourly_report import hourly_report_loop
from app.telegram.notifier import send_telegram_message
from sqlalchemy import text
from app.database.session import SessionLocal
from app.trading_executor import execute_paper_trade
from app.exchange.bitvavo_public import get_ticker_price
from app.strategies.simple_momentum import generate_momentum_signal
import asyncio
from app.market_collector import market_collector_loop
from app.database.repository import save_price_tick
from app.database.init_db import init_db
from app.exchange.bitvavo_public import get_ticker_price
from fastapi import FastAPI
from app.core.settings import settings
from app.risk.manager import RiskManager
from app.risk.models import RiskContext

app = FastAPI(title="Bitvavo AI Trading Bot")
templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def on_startup():
    init_db()
    asyncio.create_task(market_collector_loop())
    asyncio.create_task(hourly_report_loop())
    asyncio.create_task(trading_loop())


@app.get("/")
def home():
    return {
        "status": "running",
        "app": "Bitvavo AI Trading Bot",
        "environment": settings.app_env,
        "paper_trading": settings.paper_trading,
        "pairs": settings.trading_pairs.split(","),
        "base_currency": settings.base_currency,
    }


@app.get("/health")
def health():
    return {
        "ok": True,
        "paper_trading": settings.paper_trading,
    }


@app.get("/config/safety")
def safety_config():
    return {
        "paper_trading": settings.paper_trading,
        "max_position_eur": settings.max_position_eur,
        "max_daily_loss_eur": settings.max_daily_loss_eur,
        "risk_per_trade_percent": settings.risk_per_trade_percent,
    }


@app.get("/market/{market}/price")
async def market_price(market: str):
    data = await get_ticker_price(market.upper())
    tick = save_price_tick(data["market"], float(data["price"]))

    return {
        "market": data["market"],
        "price": data["price"],
        "saved": True,
        "tick_id": tick.id,
    }


@app.get("/strategy/{market}/momentum")
def momentum_strategy(market: str):
    signal = generate_momentum_signal(market.upper())

    if signal is None:
        return {
            "market": market.upper(),
            "signal": "WAIT",
            "reason": "Nog niet genoeg prijsdata.",
        }

    return {
        "market": signal.market,
        "signal": signal.signal,
        "confidence": signal.confidence,
        "reason": signal.reason,
        "signal_id": signal.id,
    }


@app.post("/trade/{market}/paper")
async def paper_trade(market: str):
    signal = generate_combined_signal(market.upper())

    if signal.signal == "HOLD":
        return {
            "market": market.upper(),
            "executed": False,
            "reason": "Geen BUY/SELL signaal.",
            "signal": signal.signal,
            "signal_id": signal.id,
        }

    risk_manager = RiskManager()
    risk_decision = risk_manager.evaluate(
        RiskContext(
            paper_trading=settings.paper_trading,
            has_open_position=False,
            daily_loss=0.0,
            max_daily_loss=settings.max_daily_loss_eur,
            cooldown_active=False,
            position_size=settings.max_position_eur,
            max_position_size=settings.max_position_eur,
        )
    )

    if not risk_decision.allowed:
        return {
            "market": market.upper(),
            "executed": False,
            "reason": risk_decision.reason,
            "signal": signal.signal,
            "signal_id": signal.id,
            "risk_allowed": risk_decision.allowed,
        }

    price_data = await get_ticker_price(market.upper())

    trade = execute_paper_trade(
        market=market.upper(),
        side=signal.signal,
        price=float(price_data["price"]),
    )

    return {
        "executed": True,
        "paper_trade": True,
        "trade_id": trade.id,
        "market": trade.market,
        "side": trade.side,
        "amount_eur": trade.amount_eur,
        "price": trade.price,
        "signal": signal.signal,
        "signal_id": signal.id,
        "risk_allowed": risk_decision.allowed,
        "risk_reason": risk_decision.reason,
    }


@app.get("/overview/signals")
def latest_signals():
    db = SessionLocal()
    try:
        rows = db.execute(text("""
            SELECT id, market, signal, confidence, reason, created_at
            FROM trade_signals
            ORDER BY id DESC
            LIMIT 10
        """)).fetchall()

        return [
            {
                "id": row[0],
                "market": row[1],
                "signal": row[2],
                "confidence": row[3],
                "reason": row[4],
                "created_at": str(row[5]),
            }
            for row in rows
        ]
    finally:
        db.close()


@app.get("/overview/paper-trades")
def latest_paper_trades():
    db = SessionLocal()
    try:
        rows = db.execute(text("""
            SELECT id, market, side, amount_eur, price, executed, created_at
            FROM paper_trades
            ORDER BY id DESC
            LIMIT 10
        """)).fetchall()

        return [
            {
                "id": row[0],
                "market": row[1],
                "side": row[2],
                "amount_eur": row[3],
                "price": row[4],
                "executed": row[5],
                "created_at": str(row[6]),
            }
            for row in rows
        ]
    finally:
        db.close()


@app.post("/telegram/test")
async def telegram_test():
    result = await send_telegram_message(
        "✅ Bitvavo AI Trading Bot is verbonden met Telegram."
    )
    return result


@app.get("/analysis/{market}/trend")
def trend_analysis(market: str):
    return calculate_trend_score(market.upper())


@app.get("/signal/{market}/combined")
def combined_signal(market: str):
    signal = generate_combined_signal(market.upper())
    return {
        "market": signal.market,
        "signal": signal.signal,
        "confidence": signal.confidence,
        "reason": signal.reason,
        "signal_id": signal.id,
    }


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    db = SessionLocal()
    try:
        latest_signal = db.execute(text("""
            SELECT id, market, signal, confidence, reason, created_at
            FROM trade_signals
            ORDER BY id DESC
            LIMIT 1
        """)).fetchone()

        latest_trade = db.execute(text("""
            SELECT id, market, side, amount_eur, price, executed, created_at
            FROM paper_trades
            ORDER BY id DESC
            LIMIT 1
        """)).fetchone()

        latest_price = db.execute(text("""
            SELECT market, price, created_at
            FROM price_ticks
            ORDER BY id DESC
            LIMIT 1
        """)).fetchone()

        paper_trade_count = db.execute(text("""
            SELECT COUNT(*)
            FROM paper_trades
        """)).scalar()

        buys_total = db.execute(text("""
            SELECT COALESCE(SUM(amount_eur), 0)
            FROM paper_trades
            WHERE side = 'BUY'
        """)).scalar()

        sells_total = db.execute(text("""
            SELECT COALESCE(SUM(amount_eur), 0)
            FROM paper_trades
            WHERE side = 'SELL'
        """)).scalar()

        cash_balance = (
            settings.paper_start_balance_eur - float(buys_total) + float(sells_total)
        )

        buy_count = db.execute(text("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE side = 'BUY'
        """)).scalar()

        sell_count = db.execute(text("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE side = 'SELL'
        """)).scalar()

        open_position_value = 0.0
        if buy_count > sell_count:
            open_position_value = settings.max_position_eur

        portfolio_value = cash_balance + open_position_value
        portfolio_pnl = portfolio_value - settings.paper_start_balance_eur
        portfolio_growth_percent = (
            portfolio_pnl / settings.paper_start_balance_eur
        ) * 100

        performance = db.execute(text("""
            WITH ordered_trades AS (
                SELECT
                    id,
                    side,
                    amount_eur,
                    price,
                    ROW_NUMBER() OVER (ORDER BY id) AS rn
                FROM paper_trades
                WHERE market = 'BTC-EUR'
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
        """)).fetchone()

        closed_trades = performance[0]
        total_pnl_eur = float(performance[1])
        avg_pnl_eur = float(performance[2])
        winning_trades = performance[3]

        if closed_trades > 0:
            winrate = (winning_trades / closed_trades) * 100
        else:
            winrate = 0.0

        risk_decision = RiskManager().evaluate(
            RiskContext(
                paper_trading=settings.paper_trading,
                has_open_position=buy_count > sell_count,
                daily_loss=0.0,
                max_daily_loss=settings.max_daily_loss_eur,
                cooldown_active=False,
                position_size=settings.max_position_eur,
                max_position_size=settings.max_position_eur,
            )
        )

        status_file = Path("/tmp/trading_loop_status.txt")
        if status_file.exists():
            last_loop_run = status_file.read_text().strip()
        else:
            last_loop_run = None

        return templates.TemplateResponse(
            request=request,
            name="dashboard.html",
            context={
                "title": "Project Atlas Dashboard",
                "paper_trading": settings.paper_trading,
                "latest_signal": latest_signal,
                "latest_trade": latest_trade,
                "latest_price": latest_price,
                "paper_trade_count": paper_trade_count,
                "risk_decision": risk_decision,
                "last_loop_run": last_loop_run,
                "max_position_eur": settings.max_position_eur,
                "paper_start_balance_eur": settings.paper_start_balance_eur,
                "cash_balance": cash_balance,
                "open_position_value": open_position_value,
                "portfolio_value": portfolio_value,
                "portfolio_pnl": portfolio_pnl,
                "portfolio_growth_percent": portfolio_growth_percent,
                "closed_trades": closed_trades,
                "total_pnl_eur": total_pnl_eur,
                "avg_pnl_eur": avg_pnl_eur,
                "winrate": winrate,
            },
        )
    finally:
        db.close()


@app.post("/trade/{market}/test-sell")
async def test_sell_trade(market: str):
    price_data = await get_ticker_price(market.upper())

    trade = execute_paper_trade(
        market=market.upper(),
        side="SELL",
        price=float(price_data["price"]),
    )

    return {
        "executed": True,
        "paper_trade": True,
        "test_mode": True,
        "trade_id": trade.id,
        "market": trade.market,
        "side": trade.side,
        "amount_eur": trade.amount_eur,
        "price": trade.price,
    }
