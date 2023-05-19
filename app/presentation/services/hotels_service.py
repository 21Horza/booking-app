from datetime import date

from sqlalchemy import and_, func, or_, select

from app.domain.entities.bookings.model.booking_model import Bookings
from app.domain.entities.hotels.model.hotel_model import Hotels
from app.domain.entities.rooms.model.room_model import Rooms
from app.infrastructure.database.database import async_session_maker

from ..services.base_service import BaseService


class HotelsService(BaseService):
    model = Hotels

    @classmethod
    async def get_all(cls, location: str, date_from: date, date_to: date):
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
                .select_from(Bookings)
                .where(
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    ),
                )
                .group_by(Bookings.room_id)
                .cte("booked_rooms")
            )

            booked_hotels = (
                select(Rooms.hotel_id, func.sum(
                        Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                ).label("rooms_left"))
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .group_by(Rooms.hotel_id)
                .cte("booked_hotels")
            )


            get_hotels_with_rooms = (
                    select(
                    Hotels.__table__.columns,
                    booked_hotels.c.rooms_left,
                )
                .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
                .where(
                    and_(
                        booked_hotels.c.rooms_left > 0,
                        Hotels.location.contains(location),
                    )
                )
            )
            
            async with async_session_maker() as session:
                hotels_with_rooms = await session.execute(get_hotels_with_rooms)
                return hotels_with_rooms.mappings().all()
        