from aiohttp import web
from frontend.app import app
import asyncio

async def run():
    runner = web.AppRunner(app())
    await runner.setup()
    site = web.TCPSite(runner, host="0.0.0.0", port=8000)    
    await site.start()
    print("started site")
    await asyncio.Future()