import asyncio
from functools import wraps
from datetime import datetime, timedelta
import os
from fastapi import HTTPException
import redis.asyncio as aioredis

class RateLimiter:
    def __init__(self):
        self.redis = aioredis.Redis.from_url(os.getenv("REDIS_URL", "redis://localhost"))

    async def is_rate_limited(self, key: str, limit: int, window: int) -> bool:
        current = await self.redis.incr(key)
        if current == 1:
            await self.redis.expire(key, window)
        return current > limit

def rate_limit(limit: int, window: int):
    limiter = RateLimiter()
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"rate_limit:{func.__name__}"
            if await limiter.is_rate_limited(key, limit, window):
                raise HTTPException(status_code=429, detail="Too many requests")
            return await func(*args, **kwargs)
        return wrapper
    return decorator