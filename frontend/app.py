from aiohttp import web
from backend.auth_socket import auth_socket

async def index(request):
    return web.FileResponse("frontend/index.html")

def app():
    app = web.Application()
    app.add_routes([
        web.static('/static', "frontend/static/"),
        web.get('/ws', auth_socket),
        web.get('/', index)
    ])
    return app