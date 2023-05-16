from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.routes.bookings_router import router as bookings_router
from app.presentation.routes.users_router import router as users_router
from app.presentation.routes.hotels_router import router as hotels_router
from app.presentation.routes.rooms_router import router as rooms_router
from app.presentation.pages.pages_router import router as pages_router
from app.presentation.images.images_router import router as images_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/presentation/static"), "static")

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)

app.include_router(pages_router)
app.include_router(images_router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[
        "GET", 
        "POST", 
        "OPTIONS", 
        "DELETE", 
        "PATCH", 
        "PUT"
    ],
    allow_headers=[
        "Content-Type", 
        "Set-Cookie", 
        "Access-Control-Allow-Headers", 
        "Access-Control-Allow-Origin",
        "Authorization"
    ],
)

@app.on_event("startup")
def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="cache")