from aiohttp import web

async def index(request):
    return web.FileResponse("frontend/index.html")

def app():
    app = web.Application()
    app.add_routes([
        web.static('/static/', "frontend/static"),
        web.get('/', index)
    ])
    return app