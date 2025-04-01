from aiohttp import web
from backend.auth_socket import auth_socket
from backend.login import login

async def index(request):
    return web.FileResponse("frontend/html/index.html")

async def login_frontend(request):
    return web.FileResponse("frontend/html/login.html")

def app():
    app = web.Application()
    app.add_routes([
        web.static('/static', "frontend/static/"),
        web.post('/login', login),
        web.get('/login', login_frontend),
        web.get('/ws', auth_socket),
        web.get('/', index)
    ])
    return app