import json

from backend.proxy import proxy_servers
import backend.auth as IPAuth
import data.token
import data.db

async def handle_auth(ws, state, event):
    if not state["authed"]:
        user = data.token.decode_jwt(event["token"])
        if user is not None:
            state["authed"] = True
            state["user"] = user["user"]
            IPAuth.add(state["ip"])
            await ws.send_str(json.dumps({
                "type": "auth",
                "status": "OK",
                "msg": state["user"]
            }))
        else:
            await ws.send_str(json.dumps({
                "type": "auth",
                "status": "Invalid token"
            }))
    else:
        await ws.send_str(json.dumps({
            "type": "auth",
            "status": "Already authed"
        }))

async def handle_change_pw(ws, state, event):
    if state["authed"]:
        new_password = event["password"]
        if data.db.update_password(state["user"], new_password):
            await ws.send_str(json.dumps({
                "type": "change-pw",
                "status": "OK"
            }))
        else:
            await ws.send_str(json.dumps({
                "type": "change-pw",
                "status": "FAIL"
            }))
    else:
        await ws.send_str(json.dumps({
            "type": "change-pw",
            "status": "Not logged in"
        }))

async def handle_new_port(ws, state, event):
    if state["authed"]:
        proxy_port = event["proxy_port"]
        hidden_port = event["hidden_port"]
        if proxy_port in proxy_servers:
            proxy_servers[proxy_port].close()
            del proxy_servers[proxy_port]
        proxy_servers[proxy_port] = ProxyServer()
        data.db.add_port(proxy_port, hidden_port, False)
        await ws.send_str(json.dumps({
            "type": "new-port",
            "status": "OK"
        }))
    else:
        await ws.send_str(json.dumps({
            "type": "new-port",
            "status": "Not logged in"
        }))

async def get_authed_ports(ws, state, event):
    if state["authed"]:
        ports = data.db.get_all_ports(state["user"])
        list_ports = [[port["proxy_port"], port["hidden_port"]] for port in ports]
        await ws.send_str(json.dumps({
            "type": "get-ports",
            "status": "OK",
            "msg": list_ports
        }))
    else:
        await ws.send_str(json.dumps({
            "type": "get-ports",
            "status": "Not logged in"
        }))