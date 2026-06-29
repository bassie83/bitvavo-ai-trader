from app.core.settings import settings
from app.database.models import PaperTrade
from app.database.session import SessionLocal


def execute_paper_trade(market: str, side: str, price: float) -> PaperTrade:
    if not settings.paper_trading:
        raise RuntimeError("Live trading is nog niet ondersteund. Veiligheid: alleen paper trading.")

    db = SessionLocal()
    try:
        trade = PaperTrade(
            market=market,
            side=side,
            amount_eur=settings.max_position_eur,
            price=price,
            executed=True,
        )
        db.add(trade)
        db.commit()
        db.refresh(trade)
        return trade
    finally:
        db.close()
