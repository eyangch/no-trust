#!/usr/bin/env python3

# Simple TCP proxy server
# 
# This script can be used to route traffic from one host to another.
#
# Example:
# proxy.py 127.0.0.1 8080 example.org 80
#
# Running the command above will start a TCP server listening on 127.0.0.1:8080.
# When a client connects to it, it will start a connection to example.org:80, and
# proxy the data from the client to the target, and from the target back to the client.

import asyncio
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosedOK
import sys

import backend

if __name__ == "__main__":
    asyncio.run(backend.run())
