from app.database.models import PriceTick
from app.database.session import SessionLocal


def save_price_tick(market: str, price: float) -> PriceTick:
    db = SessionLocal()
    try:
        tick = PriceTick(market=market, price=price)
        db.add(tick)
        db.commit()
        db.refresh(tick)
        return tick
    finally:
        db.close()
