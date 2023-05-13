from fastapi import status, HTTPException

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="No available rooms left"
)