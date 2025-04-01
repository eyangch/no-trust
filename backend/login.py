from aiohttp import web

import data.db
import data.token

async def login(request):
    json_res: dict = await request.json()
    user: str = json_res["user"]
    password: str = json_res["password"]
    if data.db.authenticate_user(user, password):
        token = data.token.gen_jwt(user, password)
        return web.json_response({"status": "OK", "token": token})
    return web.json_response({"status": "Wrong username/password"})
