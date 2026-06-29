import asyncio
import logging

from app.core.settings import settings
from app.database.repository import save_price_tick
from app.exchange.bitvavo_public import get_ticker_price

logger = logging.getLogger("market_collector")


async def collect_market_price(market: str) -> None:
    try:
        data = await get_ticker_price(market)
        tick = save_price_tick(data["market"], float(data["price"]))
        logger.info("Saved price tick %s %s id=%s", data["market"], data["price"], tick.id)
    except Exception as exc:
        logger.exception("Failed to collect price for %s: %s", market, exc)


async def market_collector_loop() -> None:
    markets = [m.strip().upper() for m in settings.trading_pairs.split(",") if m.strip()]

    while True:
        for market in markets:
            await collect_market_price(market)

        await asyncio.sleep(60)
