from app.application.entities.bookings.model.bookings_model import Bookings
from .base_service import BaseService

class BookingsService(BaseService):
    model = Bookings
    