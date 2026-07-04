from dataclasses import dataclass
from typing import Any


@dataclass
class MarketContext:
    """
    Complete market context for a single trading decision.
    """

    market: str

    technical: Any
    sentiment: Any
    news: Any
    portfolio: Any
    risk: Any


from datetime import datetime


def build_market_context(
    market: str,
    technical,
    sentiment,
    news,
    portfolio,
    risk,
) -> MarketContext:
    """
    Build a complete market context for Atlas Brain.
    """

    return MarketContext(
        market=market,
        technical=technical,
        sentiment=sentiment,
        news=news,
        portfolio=portfolio,
        risk=risk,
    )
