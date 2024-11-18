import os
from redis import asyncio as aioredis
import json

class Cache:
    def __init__(self):
        self.redis = None

    async def connect(self):
        try:
            self.redis = await aioredis.from_url(
                os.getenv("REDIS_URL", "redis://cache"),
                encoding="utf-8",
                decode_responses=True
            )
        except Exception as e:
            print(f"Redis connection error: {e}")
            raise

    async def disconnect(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key: str):
        if self.redis:
            value = await self.redis.get(key)
            return json.loads(value) if value else None
        return None

    async def set(self, key: str, value: dict, expire: int = 3600):
        if self.redis:
            await self.redis.set(key, json.dumps(value), ex=expire)

__all__ = ['cache']
cache = Cache()