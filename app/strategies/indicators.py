from sqlalchemy import text
from app.database.session import SessionLocal


def get_recent_prices(market: str, limit: int = 50) -> list[float]:
    db = SessionLocal()
    try:
        rows = db.execute(
            text("""
                SELECT price
                FROM price_ticks
                WHERE market = :market
                ORDER BY id DESC
                LIMIT :limit
            """),
            {"market": market, "limit": limit},
        ).fetchall()

        return [float(row[0]) for row in rows][::-1]
    finally:
        db.close()


def simple_moving_average(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def exponential_moving_average(values: list[float], period: int) -> float | None:
    if len(values) < period:
        return None

    multiplier = 2 / (period + 1)
    ema = sum(values[:period]) / period

    for price in values[period:]:
        ema = (price - ema) * multiplier + ema

    return ema


def calculate_rsi(values: list[float], period: int = 14) -> float | None:
    if len(values) < period + 1:
        return None

    gains = []
    losses = []

    for i in range(1, period + 1):
        change = values[-i] - values[-i - 1]
        if change >= 0:
            gains.append(change)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(abs(change))

    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period

    if avg_loss == 0:
        return 100.0

    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def calculate_macd(values: list[float]) -> dict | None:
    if len(values) < 26:
        return None

    ema_12 = exponential_moving_average(values, 12)
    ema_26 = exponential_moving_average(values, 26)

    if ema_12 is None or ema_26 is None:
        return None

    macd = ema_12 - ema_26

    return {
        "macd": macd,
        "ema_12": ema_12,
        "ema_26": ema_26,
        "signal": "BULLISH" if macd > 0 else "BEARISH",
    }


def calculate_trend_score(market: str) -> dict:
    prices = get_recent_prices(market, 30)

    if len(prices) < 10:
        return {
            "market": market,
            "ready": False,
            "reason": "Nog niet genoeg prijsdata voor trendanalyse.",
        }

    latest = prices[-1]
    first = prices[0]

    sma_short = simple_moving_average(prices[-10:])
    sma_long = simple_moving_average(prices)
    ema_20 = exponential_moving_average(prices, 20)
    rsi = calculate_rsi(prices, 14)
    macd_data = calculate_macd(prices)

    change_percent = ((latest - first) / first) * 100
    score = 50

    if sma_short is not None and sma_long is not None:
        score += 10 if latest > sma_short else -10
        score += 15 if sma_short > sma_long else -15

    if ema_20 is not None:
        score += 10 if latest > ema_20 else -10

    if change_percent > 0.2:
        score += 15
    elif change_percent < -0.2:
        score -= 15

    if rsi is not None:
        if rsi < 30:
            score += 10
        elif rsi > 70:
            score -= 10

    if macd_data is not None:
        score += 10 if macd_data["macd"] > 0 else -10

    score = max(0, min(100, score))

    if score >= 70:
        advice = "BUY_BIAS"
    elif score <= 30:
        advice = "SELL_BIAS"
    else:
        advice = "NEUTRAL"

    return {
        "market": market,
        "ready": True,
        "latest_price": latest,
        "sma_short": sma_short,
        "sma_long": sma_long,
        "ema_20": ema_20,
        "rsi": rsi,
        "macd": macd_data,
        "change_percent": change_percent,
        "score": score,
        "advice": advice,
    }
