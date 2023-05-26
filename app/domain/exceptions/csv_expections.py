from fastapi import HTTPException, status


CannotProcessCSV = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to add entry"
)

CannotAddDataToDatabase = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Failed to process CSV file"
)
