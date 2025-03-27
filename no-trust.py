import asyncio

import backend
import frontend

async def main():
    try:
        await asyncio.gather(frontend.run(), backend.run())
    except asyncio.exceptions.CancelledError:
        await asyncio.gather(backend.stop())

if __name__ == "__main__":
    asyncio.run(main())
