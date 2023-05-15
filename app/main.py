from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.presentation.routes.bookings_router import router as bookings_router
from app.presentation.routes.users_router import router as users_router
from app.presentation.routes.hotels_router import router as hotels_router
from app.presentation.routes.rooms_router import router as rooms_router
from app.presentation.pages.pages_router import router as pages_router

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/presentation/static"), "static")

app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(rooms_router)

app.include_router(pages_router)