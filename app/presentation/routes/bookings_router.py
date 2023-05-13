from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import date
from app.domain.entities.users.model.users_model import Users
from app.domain.exceptions.booking_exceptions import RoomCannotBeBooked
from ..middlewares.users_middleware import get_current_user
from ..services.bookings_service import BookingsService

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingsService.get_all(user_id=user.id)

@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user
)):
    await BookingsService.add(user.id, room_id, date_from, date_to)
