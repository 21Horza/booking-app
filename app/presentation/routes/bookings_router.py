from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import date
from app.domain.entities.users.model.users_model import Users
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
async def get_bookings(user: Users = Depends(get_current_user)): # -> list[SBooking]:
    return await BookingsService.get_all(user_id=user.id)
