import asyncio

class ProxyServer:
    async def proxy(self, stdin, stdout):    
        while True:
            line = await stdin.read(1024)
            if not line or stdout.is_closing():
                break
            stdout.write(line)
            await stdout.drain()
        stdout.close()

    async def handle_client(self, source_reader, source_writer):
        target_reader, target_writer = await asyncio.open_connection("localhost", self.fwd_port)
        await asyncio.gather(self.proxy(source_reader, target_writer), self.proxy(target_reader, source_writer))

    async def start(self, host, port, fwd_port):
        self.fwd_port = fwd_port
        self.server = await asyncio.start_server(self.handle_client, host, port)
        async with self.server:
            print(f"Serving on {host}:{port}")
            await self.server.serve_forever()

    async def close(self):
        self.server.close()
        await self.server.wait_closed()