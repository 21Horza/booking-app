import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator

from app.domain.entities.admin.admin_views import (
    BookingsAdmin,
    HotelsAdmin,
    RoomsAdmin,
    UsersAdmin,
)
from app.domain.shared.config.config import settings
from app.infrastructure.database.database import engine
from app.infrastructure.identityProviders.admin.auth_admin import authentication_backend
from app.presentation.images.images_router import router as images_router
from app.presentation.pages.pages_router import router as pages_router
from app.presentation.routes.bookings_router import router as bookings_router
from app.presentation.routes.hotels_router import router as hotels_router
from app.presentation.routes.rooms_router import router as rooms_router
from app.presentation.routes.users_router import router as users_router
from app.presentation.routes.prometheus_router import router as prometheus_router
from app.logger import logger
import sentry_sdk

app = FastAPI()

from fastapi import FastAPI

sentry_sdk.init(
    dsn="https://ff02f1c10e2f414a89eb1e8f56363a72@o4505211228192768.ingest.sentry.io/4505211232583680",

    traces_sample_rate=1.0,
)

app = FastAPI()

#server routers
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)

# client routers
app.include_router(prometheus_router)
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
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
instrumentator.instrument(app).expose(app)

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)

app.mount("/static", StaticFiles(directory="app/presentation/static"), "static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response