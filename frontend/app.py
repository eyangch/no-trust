from aiohttp import web
import asyncio

async def index(request):
    return web.FileResponse("frontend/index.html")

def app():
    app = web.Application()
    app.add_routes([
        web.static('/static/', "frontend/static"),
        web.get('/', index)
    ])
    return app