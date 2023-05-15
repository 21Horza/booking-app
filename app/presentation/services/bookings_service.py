from datetime import date
from sqlalchemy import and_, func, insert, or_, select
from app.domain.entities.bookings.model.booking_model import Bookings
from app.domain.entities.rooms.model.room_model import Rooms
from app.domain.exceptions.booking_exceptions import RoomCannotBeBooked
from app.infrastructure.database.database import engine, async_session_maker
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

        async with async_session_maker() as session:
            booked_Room = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from <= date_to
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to < date_from
                        ),
                    )
                )
            ).cte("booked_Room")

            get_Room_left = select(
                (Rooms.quantity - func.count(booked_Room.c.room_id)).label("Room_left")
                ).select_from(Rooms).join(
                    booked_Room, booked_Room.c.room_id == Rooms.id, isouter=True
                ).where(Rooms.id == 1).group_by(
                    Rooms.quantity, booked_Room.c.room_id
                )
            
            print(get_Room_left.compile(engine, compile_kwargs={"literal_binds": True}))

            Room_left = await session.execute(get_Room_left)
            Room_left: int = Room_left.scalar()

            if Room_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id = room_id,
                        user_id = user_id,
                        date_from = date_from,
                        date_to = date_to,
                        price = price
                )
                .returning(Bookings)
                )

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalars()
            else: 
                raise RoomCannotBeBooked
