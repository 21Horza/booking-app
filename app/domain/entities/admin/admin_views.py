from sqladmin import ModelView
from ...entities.rooms.model.room_model import Rooms
from ...entities.bookings.model.booking_model import Bookings
from ...entities.hotels.model.hotel_model import Hotels
from ...entities.users.model.user_model import Users

class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    can_delete = False
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [Bookings.user, Bookings.room_id]
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-book"

class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.booking]
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"

class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"