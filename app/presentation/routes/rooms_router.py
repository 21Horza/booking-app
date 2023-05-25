from datetime import date
from typing import List

from fastapi import APIRouter

from app.domain.entities.rooms.schema.room_schema import SRoomDetails
from app.presentation.services.rooms_service import RoomsService

router = APIRouter(
    prefix="/rooms",
    tags=["rooms"],
)

# get all hotels by location
# no auth required
@router.get("/{hotel_id}")
async def get_rooms_by_hotel_id(
    location: str,
    date_from: date,
    date_to: date,
) -> List[SRoomDetails]:
    rooms = await RoomsService.get_all(location, date_from, date_to)
    return rooms