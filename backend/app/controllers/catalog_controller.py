from fastapi import HTTPException
from fastapi.responses import FileResponse

from ..config import Settings
from ..models.furniture_repository import get_all_furniture, get_furniture
from ..services.media_storage import resolve_media_path
from ..views.furniture import FurnitureView


def list_furniture(settings: Settings):
    items = get_all_furniture(settings)
    return [FurnitureView.from_record(item) for item in items]


def get_media(settings: Settings, source: str, filename: str):
    path = f"{source}/{filename}"
    return FileResponse(resolve_media_path(settings, path))


def get_furniture_details(settings: Settings, furniture_id: str):
    item = get_furniture(settings, furniture_id)
    if not item:
        raise HTTPException(status_code=404, detail="Móvel não encontrado.")
    return FurnitureView.from_record(item)
