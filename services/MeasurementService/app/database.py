import os
import aiomysql
from contextlib import asynccontextmanager

class Database:
    def __init__(self):
        self._pool = None

    async def connect(self):
        if not self._pool:
            self._pool = await aiomysql.create_pool(
                host=os.getenv("DB_HOST", "database"),  
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "secret"),
                db=os.getenv("DB_NAME", "bloodpressure"),
                maxsize=20,
                autocommit=True
            )

    @asynccontextmanager
    async def connection(self):
        if not self._pool:
            await self.connect()
        async with self._pool.acquire() as conn:
            yield conn

    async def disconnect(self):
        if self._pool:
            self._pool.close()
            await self._pool.wait_closed()

db = Database()