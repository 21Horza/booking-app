import asyncio
import datetime
from datetime import date, timedelta
from typing import List, Optional

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.domain.entities.hotels.schema.hotel_schema import SHotel, SHotelInfo
from app.domain.exceptions.hotel_exceptions import (
    CannotBookHotelForLongPeriod,
    DateFromCannotBeAfterDateTo,
)

from ..services.hotels_service import HotelsService

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"],
)

# get all hotels by location
# no auth required
@router.get("/{location}")
@cache(expire=40)
async def get_hotels_by_location(
    location: str,
    date_from: date = Query(..., description=f"Ex., {datetime.datetime.now().date()}"),
    date_to: date = Query(..., description=f"Ex., {(datetime.datetime.now() + timedelta(days=14)).date()}"),
) -> List[SHotelInfo]:
    if date_from > date_to:
        raise DateFromCannotBeAfterDateTo
    if (date_to - date_from).days > 31:
        raise CannotBookHotelForLongPeriod 
    hotels = await HotelsService.get_all(location, date_from, date_to)
    return hotels

# get all hotel info
# no auth required
@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int) -> Optional[SHotel]:
    return await HotelsService.get_one_or_none(id=hotel_id)
