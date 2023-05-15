from fastapi import APIRouter, UploadFile
import shutil

router = APIRouter(
    prefix="/images",
    tags=["Images download"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    with open(f"app/presentation/static/images/{name}.webp", "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
