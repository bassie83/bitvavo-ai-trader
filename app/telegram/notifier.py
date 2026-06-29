import httpx

from app.core.settings import settings


async def send_telegram_message(message: str) -> dict:
    if not settings.telegram_bot_token or not settings.telegram_chat_id:
        return {
            "sent": False,
            "reason": "Telegram token of chat ID ontbreekt.",
        }

    url = f"https://api.telegram.org/bot{settings.telegram_bot_token}/sendMessage"

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(
            url,
            json={
                "chat_id": settings.telegram_chat_id,
                "text": message,
                "parse_mode": "HTML",
            },
        )
        response.raise_for_status()
        return response.json()
