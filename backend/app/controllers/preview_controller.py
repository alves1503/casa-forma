import base64
import logging

from fastapi import HTTPException, UploadFile
from starlette.concurrency import run_in_threadpool

from ..config import Settings
from ..models.furniture_repository import get_furniture
from ..services.image_service import ImageGenerationError, create_room_preview
from ..services.image_validation import MAX_ROOM_IMAGE_BYTES, detect_image_format
from ..services.media_storage import resolve_media_path
from ..views.preview import PreviewView

logger = logging.getLogger(__name__)


async def generate_preview(
    settings: Settings,
    room_photo: UploadFile,
    furniture_id: str,
):
    furniture = get_furniture(settings, furniture_id)
    if not furniture:
        raise HTTPException(status_code=404, detail="Móvel não encontrado.")

    room_bytes = await room_photo.read(MAX_ROOM_IMAGE_BYTES + 1)
    if not room_bytes:
        raise HTTPException(status_code=400, detail="Selecione uma foto do cômodo.")
    if len(room_bytes) > MAX_ROOM_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="A imagem deve ter no máximo 16 MB.")
    room_content_type, _ = detect_image_format(room_bytes)
    if room_photo.content_type and room_content_type != room_photo.content_type:
        raise HTTPException(status_code=400, detail="O tipo do arquivo enviado não corresponde à imagem.")

    furniture_image = resolve_media_path(settings, furniture["photo_path"]).read_bytes()
    furniture_content_type, _ = detect_image_format(furniture_image)
    try:
        image = await run_in_threadpool(
            create_room_preview,
            room_bytes,
            room_content_type,
            furniture_image,
            furniture_content_type,
            furniture,
            settings.openai_api_key,
            settings.image_model,
        )
    except ImageGenerationError as error:
        logger.warning("Image preview generation failed: %s", error)
        raise HTTPException(status_code=503, detail=str(error)) from error

    return PreviewView(image=f"data:image/png;base64,{base64.b64encode(image).decode('ascii')}")
