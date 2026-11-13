from fastapi import APIRouter, Request
from fastapi.responses import FileResponse

from ..controllers import catalog_controller
from ..views.furniture import FurnitureView

router = APIRouter()


@router.get("/api/furniture", response_model=list[FurnitureView])
def list_furniture(request: Request):
    return catalog_controller.list_furniture(request.app.state.settings)


@router.get("/media/{source}/{filename}")
def get_media(source: str, filename: str, request: Request) -> FileResponse:
    return catalog_controller.get_media(request.app.state.settings, source, filename)


@router.get("/api/furniture/{furniture_id}", response_model=FurnitureView)
def get_furniture_details(furniture_id: str, request: Request):
    return catalog_controller.get_furniture_details(
        request.app.state.settings,
        furniture_id,
    )
