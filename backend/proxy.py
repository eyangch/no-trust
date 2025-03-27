import asyncio

import backend.auth as IPAuth

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
        ip = source_writer.get_extra_info("peername")
        if not IPAuth.exist(ip):
            print(f"declined ip {ip[0]}")
            source_writer.close()
            return
        print(f"proxying ip {ip[0]}")
        target_reader, target_writer = await asyncio.open_connection("localhost", self.fwd_port)
        IPAuth.add_readers(ip, [source_writer, target_writer])
        await asyncio.gather(self.proxy(source_reader, target_writer), self.proxy(target_reader, source_writer))
        IPAuth.remove_readers(ip)

    async def start(self, host, port, fwd_port):
        self.fwd_port = fwd_port
        self.server = await asyncio.start_server(self.handle_client, host, port)
        async with self.server:
            print(f"Serving on {host}:{port}")
            await self.server.serve_forever()

    async def close(self):
        self.server.close()
        await self.server.wait_closed()