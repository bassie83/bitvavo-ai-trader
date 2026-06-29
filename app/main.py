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

@app.on_event("startup")
def on_startup():
    init_db()
    asyncio.create_task(market_collector_loop())
    asyncio.create_task(hourly_report_loop())

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
            "reason": "Nog niet genoeg prijsdata."
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
