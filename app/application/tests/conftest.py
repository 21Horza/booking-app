import asyncio
import datetime
import json

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from app.domain.entities.bookings.model.booking_model import Bookings
from app.domain.entities.hotels.model.hotel_model import Hotels
from app.domain.entities.rooms.model.room_model import Rooms
from app.domain.entities.users.model.user_model import Users
from app.domain.shared.config.config import settings
from app.infrastructure.database.database import Base, async_session_maker, engine
from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_data(model: str):
        with open(f"app/application/tests/mock_data/{model}.json", encoding="utf-8") as file:
            print(f"app/application/tests/mock_data/{model}.json")
            return json.load(file)
        
    hotels = open_mock_data("hotels")
    rooms = open_mock_data("rooms")
    users = open_mock_data("users")
    bookings = open_mock_data("bookings")

    for booking in bookings:
        booking["date_from"] = datetime.datetime.strptime(booking["date_from"], "%Y-%m-%d")
        booking["date_to"] = datetime.datetime.strptime(booking["date_to"], "%Y-%m-%d")


    async with async_session_maker() as session:
        add_hotels = insert(Hotels).values(hotels)
        add_rooms = insert(Rooms).values(rooms)
        add_users = insert(Users).values(users)
        add_bookings = insert(Bookings).values(bookings)

        await session.execute(add_hotels)
        await session.execute(add_rooms)
        await session.execute(add_users)
        await session.execute(add_bookings)

        await session.commit()

# Official docs pytest-asyncio
# Create new event loop to run all tests
@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
# async client to test endpoints
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac

@pytest.fixture(scope="session")
async def auth_ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        await ac.post("/auth/login", json={
            "email": "test@test.com",
            "pwd": "test",
        })
        assert ac.cookies["access_token"]
        yield ac
