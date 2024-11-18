from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import measurement_routes
from app.database import db

import prometheus_client

from app.cache import Cache 

cache = Cache() 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    await cache.connect()
    yield
    await db.disconnect()
    await cache.disconnect()
    await cache.disconnect()

app = FastAPI(lifespan=lifespan)

#cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#routes
app.include_router(measurement_routes.router, prefix="/api/v1")

#metrics ep
@app.get("/metrics")
async def metrics():
    return prometheus_client.generate_latest()

#checking the nice health :)
@app.get("/health")
async def health():
    try:
        await db.ping()
        await cache.ping()
        return {"status": "healthy"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}