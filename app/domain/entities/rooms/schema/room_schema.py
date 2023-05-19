from datetime import date

from pydantic import BaseModel


class SRoom(BaseModel):
    id: str
    hotel_id: int
    name: str
    description: str
    price: int
    quantity: int
    services: list[str]
    image_id: int
    date_from: date
    date_to: date

    class Config:
        orm_mode = True

class SRoomDetails(SRoom):
    total_cost: int
    rooms_left: int

    class Config:
        orm_mode = True