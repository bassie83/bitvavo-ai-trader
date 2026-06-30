from sqlalchemy import text
from app.database.session import SessionLocal
import asyncio
from datetime import datetime
from app.core.settings import settings
from app.exchange.bitvavo_public import get_ticker_price
from app.risk.manager import RiskManager
from app.risk.models import RiskContext
from app.strategies.signal_engine import generate_combined_signal
from app.trading_executor import execute_paper_trade

def has_open_position(market: str) -> bool:
    db = SessionLocal()
    try:
        buys = db.execute(text("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE market = :market AND side = 'BUY'
        """), {"market": market}).scalar()

        sells = db.execute(text("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE market = :market AND side = 'SELL'
        """), {"market": market}).scalar()

        return buys > sells
    finally:
        db.close()

async def trading_loop():
    """
    Automatische paper trading-loop.
    """

    while True:
        try:
            market = "BTC-EUR"

            print("🤖 Trading loop heartbeat: running", flush=True)

            with open("/tmp/trading_loop_status.txt", "w") as status_file:
                status_file.write(datetime.utcnow().isoformat())

            signal = generate_combined_signal(market)

            if signal.signal == "HOLD":
                print("⏸️ Trading loop: HOLD signal, no trade", flush=True)
                await asyncio.sleep(60)
                continue

            if signal.signal == "SELL" and not has_open_position(market):
                print("⏸️ Trading loop: SELL signal, but no open position", flush=True)
                await asyncio.sleep(60)
                continue

            risk_decision = RiskManager().evaluate(
                RiskContext(
                    paper_trading=settings.paper_trading,
                    has_open_position=(
                        signal.signal == "BUY"
                        and has_open_position(market)
                    ),
                    daily_loss=0.0,
                    max_daily_loss=settings.max_daily_loss_eur,
                    cooldown_active=False,
                    position_size=settings.max_position_eur,
                    max_position_size=settings.max_position_eur,
                )
            )

            if not risk_decision.allowed:
                print(
                    f"🛡️ Trading loop: blocked - {risk_decision.reason}",
                    flush=True,
                )
                await asyncio.sleep(60)
                continue

            price_data = await get_ticker_price(market)

            trade = execute_paper_trade(
                market=market,
                side=signal.signal,
                price=float(price_data["price"]),
            )

            print(
                f"✅ Paper trade executed: {trade.side} {trade.market}",
                flush=True,
            )

        except Exception as error:
            print(f"❌ Trading loop error: {error}", flush=True)

        await asyncio.sleep(60)
