from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.domain.entities.admin.admin_views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.presentation.routes.bookings_router import router as bookings_router
from app.presentation.routes.users_router import router as users_router
from app.presentation.routes.hotels_router import router as hotels_router
from app.presentation.routes.rooms_router import router as rooms_router
from app.presentation.pages.pages_router import router as pages_router
from app.presentation.images.images_router import router as images_router
from app.infrastructure.database.config import settings
from app.infrastructure.database.database import engine
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from sqladmin import Admin
from redis import asyncio as aioredis
from app.infrastructure.identityProviders.admin.auth_admin import authentication_backend

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/presentation/static"), "static")

#server routers
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)

# client routers
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
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)