from sqlalchemy import text
from app.database.session import SessionLocal
import asyncio
from datetime import datetime

from app.core.settings import settings
from app.exchange.bitvavo_public import get_ticker_price
from app.risk.manager import RiskManager
from app.risk.models import RiskContext
from app.trading_executor import execute_paper_trade

from app.intelligence.technical import get_technical_intelligence
from app.intelligence.fear_greed import get_fear_greed
from app.intelligence.brain import analyze_brain
from app.intelligence.execution_plan import build_execution_plan


def has_open_position(market: str) -> bool:
    db = SessionLocal()
    try:
        buys = db.execute(
            text("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE market = :market AND side = 'BUY'
        """),
            {"market": market},
        ).scalar()

        sells = db.execute(
            text("""
            SELECT COUNT(*)
            FROM paper_trades
            WHERE market = :market AND side = 'SELL'
        """),
            {"market": market},
        ).scalar()

        return buys > sells
    finally:
        db.close()


async def trading_loop():
    """
    Automated paper trading loop powered by the Atlas pipeline.
    """

    while True:
        try:
            market = "BTC-EUR"

            print("🤖 Trading loop heartbeat: running", flush=True)

            with open("/tmp/trading_loop_status.txt", "w") as status_file:
                status_file.write(datetime.utcnow().isoformat())

            open_position = has_open_position(market)

            technical = get_technical_intelligence(market)
            fear_greed = get_fear_greed()

            brain = analyze_brain(
                technical=technical["brain"],
                sentiment=fear_greed,
                has_open_position=open_position,
                risk_allowed=True,
            )

            execution_plan = build_execution_plan(
                market=market,
                decision=brain["decision"],
                max_position_eur=settings.max_position_eur,
            )

            print(f"🧠 Atlas Brain: {brain}", flush=True)
            print(f"📋 Execution Plan: {execution_plan}", flush=True)

            if execution_plan["action"] == "HOLD":
                print("⏸️ Trading loop: Execution Plan is HOLD, no trade", flush=True)
                await asyncio.sleep(60)
                continue

            if execution_plan["action"] == "SELL" and not open_position:
                print("⏸️ Trading loop: SELL plan, but no open position", flush=True)
                await asyncio.sleep(60)
                continue

            risk_decision = RiskManager().evaluate(
                RiskContext(
                    paper_trading=settings.paper_trading,
                    has_open_position=(
                        execution_plan["action"] == "BUY" and open_position
                    ),
                    daily_loss=0.0,
                    max_daily_loss=settings.max_daily_loss_eur,
                    cooldown_active=False,
                    position_size=execution_plan["amount_eur"],
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
                market=execution_plan["market"],
                side=execution_plan["action"],
                price=float(price_data["price"]),
            )

            print(
                f"✅ Paper trade executed: {trade.side} {trade.market}",
                flush=True,
            )

        except Exception as error:
            print(f"❌ Trading loop error: {error}", flush=True)

        await asyncio.sleep(60)
