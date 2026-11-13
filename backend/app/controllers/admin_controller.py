import logging
import uuid

from fastapi import HTTPException, UploadFile

from ..config import Settings
from ..models.furniture_repository import (
    get_all_furniture,
    get_furniture,
    update_furniture_photo,
)
from ..services.image_validation import MAX_FURNITURE_IMAGE_BYTES, detect_image_format
from ..views.furniture import FurnitureView
from ..views.preview import AdminSessionView

logger = logging.getLogger(__name__)


def admin_session(username: str):
    return AdminSessionView(authenticated=True, username=username)


def admin_furniture(settings: Settings):
    items = get_all_furniture(settings)
    return [FurnitureView.from_record(item) for item in items]


async def update_furniture_photo_endpoint(
    settings: Settings,
    furniture_id: str,
    photo: UploadFile,
):
    current = get_furniture(settings, furniture_id)
    if not current:
        raise HTTPException(status_code=404, detail="Móvel não encontrado.")

    image_bytes = await photo.read(MAX_FURNITURE_IMAGE_BYTES + 1)
    if not image_bytes:
        raise HTTPException(status_code=400, detail="Selecione uma foto para o móvel.")
    if len(image_bytes) > MAX_FURNITURE_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="A imagem deve ter no máximo 10 MB.")

    _, extension = detect_image_format(image_bytes)
    settings.upload_directory.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{extension}"
    destination = settings.upload_directory / filename
    temporary = destination.with_name(f".{filename}.tmp")
    try:
        temporary.write_bytes(image_bytes)
        temporary.replace(destination)
        updated = update_furniture_photo(
            settings,
            furniture_id,
            f"uploads/{filename}",
        )
    except OSError as error:
        logger.exception("Could not save furniture image")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível salvar a foto. Tente novamente.",
        ) from error
    finally:
        if temporary.exists():
            temporary.unlink()

    if not updated:
        destination.unlink(missing_ok=True)
        raise HTTPException(status_code=404, detail="Móvel não encontrado.")

    updated_item = get_furniture(settings, furniture_id)
    return FurnitureView.from_record(updated_item)
