import aiohttp
from aiohttp import web

import backend.auth as IPAuth
import data.token

async def auth_socket(request):
    ws = web.WebSocketResponse()
    try:
        await ws.prepare(request)
    except Exception as e:
        print("invalid ws conn")
        return web.Response()

    ip = request.get_extra_info("peername")

    authenticated = False

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if not authenticated:
                user = data.token.decode_jwt(msg.data)
                if user is not None:
                    authenticated = True
                    IPAuth.add(ip)
                    await ws.send_str("OK")
                else:
                    await ws.send_str("FAIL")
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())
            break

    print('websocket connection closed')
    if authenticated:
        IPAuth.remove(ip)

    return ws