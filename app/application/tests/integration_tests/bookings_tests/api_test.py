import pytest
from httpx import AsyncClient


@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (4, "2026-06-01", "2026-06-20", 3,  200),
    (4, "2026-06-01", "2026-06-20", 4,  200),
    (4, "2026-06-01", "2026-06-20", 5,  200),
    (4, "2026-06-01", "2026-06-20", 6,  200),
    (4, "2026-06-01", "2026-06-20", 7,  200),
    (4, "2026-06-01", "2026-06-20", 8,  200),
    (4, "2026-06-01", "2026-06-20", 9,  200),
    (4, "2026-06-01", "2026-06-20", 10,  200),
    (4, "2026-06-01", "2026-06-20", 10,  409),
    (4, "2026-06-01", "2026-06-20", 10, 409),
])
async def test_add_and_get_booking(room_id, date_from, date_to, booked_rooms, status_code, auth_ac: AsyncClient):
    response = await auth_ac.post("v1/bookings", params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })

    assert response.status_code == status_code

    response = await auth_ac.get("v1/bookings")

    assert len(response.json()) == booked_rooms

