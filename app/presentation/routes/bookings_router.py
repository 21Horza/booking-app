from fastapi import APIRouter, Depends
from datetime import date
from pydantic import parse_obj_as
from app.application.tasks.tasks import send_booking_confirmation
from app.domain.entities.bookings.schema.booking_schema import SBooking
from app.domain.entities.users.model.user_model import Users
from ..middlewares.users_middleware import get_current_user
from ..services.bookings_service import BookingsService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingsService.get_all(user_id=user.id)

@router.post("")
async def add_booking(
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user)
):
    booking = await BookingsService.add(user.id, room_id, date_from, date_to)
    booking_dict = parse_obj_as(SBooking, booking).dict()
    send_booking_confirmation.delay(booking_dict, user.email)
    return booking


# delete booking info
# auth required
@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    await BookingsService.delete(id=booking_id, user_id=user.id)
    return f"Booking with id: {booking_id} successfully deleted"

