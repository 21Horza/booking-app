from fastapi import APIRouter
from pydantic import BaseModel
from datetime import date
from app.presentation.services.bookings_service import BookingService

class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def get_bookings() -> list[SBooking]:
    return await BookingService.get_all()
