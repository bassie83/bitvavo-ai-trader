import httpx


BITVAVO_BASE_URL = "https://api.bitvavo.com/v2"


async def get_ticker_price(market: str) -> dict:
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            f"{BITVAVO_BASE_URL}/ticker/price",
            params={"market": market},
        )
        response.raise_for_status()
        return response.json()
