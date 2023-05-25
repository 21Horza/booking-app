from fastapi import status, HTTPException

DateFromCannotBeAfterDateTo = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Check-in date cannot be later than the check-out date"
)

CannotBookHotelForLongPeriod = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="It is not possible to book a hotel for more than a month"
)
