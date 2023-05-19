from fastapi import HTTPException, status

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="No available rooms left"
)