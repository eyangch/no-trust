from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK

class AuthServer:
    async def handle_client(self, websocket):
        addr = websocket.remote_address
        print(f"Connection from {addr!r}")
        while True:
            try:
                message = await websocket.recv()
            except ConnectionClosedOK:
                break
        print(f"Close the connection from {addr!r}")

    async def start(self, host, port):
        self.server = await serve(self.handle_client, host, port)
        async with self.server:
            print(f"Serving on {host}:{port}")
            await self.server.serve_forever()

    async def close(self):
        self.server.close()
        await self.server.wait_closed()