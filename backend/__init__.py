import asyncio

from backend.proxy import ProxyServer

proxy_server = ProxyServer()

async def run():
    await asyncio.gather(
        proxy_server.start("0.0.0.0", 25565, 28888)
    )

async def stop():
    print("\nClosing server")
    await asyncio.gather(
        proxy_server.close()
    )