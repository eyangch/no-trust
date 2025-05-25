import aiohttp
from aiohttp import web
import json

import backend.auth as IPAuth
import backend.socket_handlers

async def auth_socket(request):
    ws = web.WebSocketResponse()
    try:
        await ws.prepare(request)
    except Exception as e:
        print("invalid ws conn")
        return web.Response()

    state = {
        "authed": False,
        "ip": request.get_extra_info("peername"),
        "user": None
    }

    handlers = {
        "auth": backend.socket_handlers.handle_auth,
        "change-pw": backend.socket_handlers.handle_change_pw,
        "new-port": backend.socket_handlers.handle_new_port,
        "get-ports": backend.socket_handlers.get_authed_ports
    }

    try:
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                event = json.loads(msg.data)
                await handlers[event["type"]](ws, state, event)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                print('ws connection closed with exception %s' %
                    ws.exception())
                break
    finally:
        print('websocket connection closed')
        if state["authed"]:
            IPAuth.remove(state["ip"])

    return ws