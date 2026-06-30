import asyncio

from app.core.settings import settings
from app.exchange.bitvavo_public import get_ticker_price
from app.risk.manager import RiskManager
from app.risk.models import RiskContext
from app.strategies.signal_engine import generate_combined_signal
from app.trading_executor import execute_paper_trade


async def trading_loop():
    """
    Automatische paper trading-loop.

    Eerste echte versie:
    - draait elke 60 seconden
    - genereert een combined signal
    - controleert Risk Manager
    - voert alleen paper trade uit bij BUY/SELL + ALLOW
    """

    while True:
        try:
            market = "BTC-EUR"
            print("🤖 Trading loop heartbeat: running", flush=True)

            signal = generate_combined_signal(market)

            if signal.signal == "HOLD":
                print("⏸️ Trading loop: HOLD signal, no trade", flush=True)
                await asyncio.sleep(60)
                continue

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
                print(
                    f"🛡️ Trading loop: trade blocked - {risk_decision.reason}",
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
                f"✅ Paper trade executed: {trade.side} {trade.market} "
                f"€{trade.amount_eur} @ {trade.price}",
                flush=True,
            )

        except Exception as error:
            print(f"❌ Trading loop error: {error}", flush=True)

        await asyncio.sleep(60)
