from client import call_client
import asyncio

async def main():
    await call_client()

if __name__ == "__main__":
    asyncio.run(main())
