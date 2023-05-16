from fastapi import APIRouter, UploadFile
import shutil

from app.application.tasks.tasks import process_img

router = APIRouter(
    prefix="/images",
    tags=["Images download"]
)

@router.post("/hotels")
async def add_hotel_image(name: int, file: UploadFile):
    img_path = f"app/presentation/static/images/{name}.webp"
    with open(img_path, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    process_img.delay(img_path)
