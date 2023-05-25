from datetime import date

from fastapi import APIRouter, Depends
from pydantic import parse_obj_as

from app.application.tasks.tasks import send_booking_confirmation
from app.domain.entities.bookings.schema.booking_schema import SBooking, SBookingDetails, SNewBooking
from app.domain.entities.users.model.user_model import Users
from app.domain.exceptions.booking_exceptions import RoomCannotBeBooked

from ..middlewares.users_middleware import get_current_user
from ..services.bookings_service import BookingsService

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBookingDetails]:
    return await BookingsService.get_all_with_pics(user_id=user.id)

@router.post("")
async def add_booking(
    booking: SNewBooking,
    user: Users = Depends(get_current_user)
):
    booking = await BookingsService.add(user.id, booking.room_id, booking.date_from, booking.date_to)
    if not booking:
        raise RoomCannotBeBooked
    booking_dict = parse_obj_as(SNewBooking, booking).dict()
    # send_booking_confirmation.delay(booking_dict, user.email)
    return booking_dict


# delete booking info
# auth required
@router.delete("/{booking_id}")
async def delete_booking(
    booking_id: int,
    user: Users = Depends(get_current_user),
):
    await BookingsService.delete(id=booking_id, user_id=user.id)

