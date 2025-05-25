import asyncio

from backend.proxy import proxy_servers

async def run():
    await asyncio.gather(
        *[server.start() for server in proxy_servers.values()]
    )

async def stop():
    print("\nClosing server")
    await asyncio.gather(
        *[server.close() for server in proxy_servers.values()]
    )