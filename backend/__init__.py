import asyncio

from backend.auth import AuthServer
from backend.proxy import ProxyServer

auth_server = AuthServer()
proxy_server = ProxyServer()

async def run():
    await asyncio.gather(
        auth_server.start("0.0.0.0", 8080),
        proxy_server.start("0.0.0.0", 25565, 28888)
    )

async def stop():
    print("\nClosing server")
    await asyncio.gather(
        auth_server.close(),
        proxy_server.close()
    )