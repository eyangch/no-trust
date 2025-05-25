import asyncio

import backend.auth as IPAuth
import data.db

class ProxyServer:
    def __init__(self, host, port, hidden_host, hidden_port):
        self.host = host
        self.port = port
        self.hidden_host = hidden_host
        self.hidden_port = hidden_port

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
        target_reader, target_writer = await asyncio.open_connection(self.hidden_host, self.hidden_port)
        IPAuth.add_readers(ip, [source_writer, target_writer])
        await asyncio.gather(self.proxy(source_reader, target_writer), self.proxy(target_reader, source_writer))
        IPAuth.remove_readers(ip)

    async def start(self):
        self.server = await asyncio.start_server(self.handle_client, self.host, self.port)
        async with self.server:
            print(f"Serving on {self.host}:{self.port}")
            await self.server.serve_forever()

    async def close(self):
        self.server.close()
        await self.server.wait_closed()

proxy_servers = {}
all_ports = data.db.get_all_ports("root")
for port in all_ports:
    proxy_servers[port["proxy_port"]] = ProxyServer("0.0.0.0", port["proxy_port"], "localhost", port["hidden_port"])