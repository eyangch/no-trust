import asyncio

from backend.auth import AuthServer
from backend.proxy import ProxyServer

async def run():
    auth_server = AuthServer()
    proxy_server = ProxyServer()
    try:
        await asyncio.gather(
            auth_server.start("0.0.0.0", 8080),
            proxy_server.start("0.0.0.0", 25565, 28888)
        )
    except asyncio.exceptions.CancelledError:
        print("\nClosing server")
        await asyncio.gather(
            auth_server.close(),
            proxy_server.close()
        )