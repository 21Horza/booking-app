from datetime import date

from sqlalchemy import and_, func, insert, or_, select
from sqlalchemy.exc import SQLAlchemyError

from app.domain.entities.bookings.model.booking_model import Bookings
from app.domain.entities.rooms.model.room_model import Rooms
from app.domain.exceptions.booking_exceptions import RoomCannotBeBooked
from app.infrastructure.database.database import async_session_maker
from app.logger import logger

from .base_service import BaseService


class BookingsService(BaseService):
    model = Bookings

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        try:
            async with async_session_maker() as session:
                booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
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
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(
                    (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                        "rooms_left"
                    )
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True}))

            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings.id, Bookings.user_id, Bookings.room_id)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.mappings().one()
            else:
                raise RoomCannotBeBooked
        except (SQLAlchemyError, Exception) as err:
                if isinstance(err, SQLAlchemyError):
                    msg = "Database"
                elif isinstance(err, Exception):
                    msg = "Unknown"
                    msg += "exception: Cannot add booking"
                    extra = {
                        "user_id": user_id,
                        "room_id": room_id,
                        "date_from": date_from,
                        "date_to": date_to,
                    }
                logger.error(
                    msg, 
                    extra=extra, 
                    exc_info=True,
                )
