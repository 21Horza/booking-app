from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from ..routes.hotels_router import get_hotels_by_location

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"]
)

templates = Jinja2Templates(directory="app/presentation/templates")

@router.get("/hotels")
async def get_hotels_page(
    req: Request,
    hotels=Depends(get_hotels_by_location)
):
    return templates.TemplateResponse(
        name="hotels.html", 
        context={"request": req, "hotels": hotels},
    )