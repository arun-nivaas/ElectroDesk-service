import asyncio
import httpx


class KeepAlive:
    def __init__(self, RENDER_URL: str):
        self.RENDER_URL = RENDER_URL

    async def start(self):
        """Pings the app every 10 minutes to prevent Render sleep"""
        await asyncio.sleep(60)  # wait 1 minute after startup first
        while True:
            try:
                if self.RENDER_URL:
                    async with httpx.AsyncClient() as client:
                        await client.get(f"{self.RENDER_URL}/health")
                        print(f"Keep alive ping sent to {self.RENDER_URL}/health")
            except Exception as e:
                print(f"Keep alive ping failed: {e}")
            await asyncio.sleep(600)  # ping every 10 minutes