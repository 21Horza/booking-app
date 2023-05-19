from datetime import datetime

from app.presentation.services.bookings_service import BookingsService


async def test_add_and_get_booking():
    new_booking = await BookingsService.add(
        user_id = 2,
        room_id = 2,
        date_from = datetime.strptime("2023-07-10", "%Y-%m-%d"),
        date_to = datetime.strptime("2023-07-24", "%Y-%m-%d"),
    )

    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    await BookingsService.get_one_by_id(new_booking.id)

    assert new_booking is not None