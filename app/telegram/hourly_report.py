import asyncio
from sqlalchemy import text

from app.core.settings import settings
from app.database.session import SessionLocal
from app.telegram.notifier import send_telegram_message


def build_hourly_report() -> str:
    db = SessionLocal()
    try:
        prices = db.execute(text("""
            SELECT DISTINCT ON (market) market, price, created_at
            FROM price_ticks
            ORDER BY market, id DESC
        """)).fetchall()

        signals = db.execute(text("""
            SELECT market, signal, confidence, reason, created_at
            FROM trade_signals
            ORDER BY id DESC
            LIMIT 5
        """)).fetchall()

        price_lines = "\n".join(
            [f"• {p[0]}: €{p[1]} ({p[2]})" for p in prices]
        ) or "Geen prijsdata."

        signal_lines = "\n".join(
            [f"• {s[0]}: {s[1]} ({s[2]:.2f}) — {s[3]}" for s in signals]
        ) or "Geen signalen."

        return f"""
🤖 <b>Bitvavo AI Trading Bot - Uurupdate</b>

<b>Mode:</b> {'Paper trading' if settings.paper_trading else 'LIVE'}
<b>Max positie:</b> €{settings.max_position_eur}
<b>Max dagverlies:</b> €{settings.max_daily_loss_eur}

📈 <b>Laatste prijzen</b>
{price_lines}

📊 <b>Laatste signalen</b>
{signal_lines}
""".strip()
    finally:
        db.close()


async def hourly_report_loop() -> None:
    while True:
        report = build_hourly_report()
        await send_telegram_message(report)
        await asyncio.sleep(3600)
