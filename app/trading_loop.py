import asyncio


async def trading_loop():
    """
    Automatische trading-loop.

    Eerste versie:
    - draait elke 60 seconden
    - logt alleen dat hij actief is
    - voert nog geen trades uit
    """

    while True:
        print("🤖 Trading loop heartbeat: running", flush=True)
        await asyncio.sleep(60)
