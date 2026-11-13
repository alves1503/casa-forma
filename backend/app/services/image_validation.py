import io

from fastapi import HTTPException
from PIL import Image, UnidentifiedImageError

IMAGE_FORMATS = {
    "JPEG": ("image/jpeg", ".jpg"),
    "PNG": ("image/png", ".png"),
    "WEBP": ("image/webp", ".webp"),
}
MAX_ROOM_IMAGE_BYTES = 16 * 1024 * 1024
MAX_FURNITURE_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 40_000_000


def detect_image_format(image_bytes: bytes):
    try:
        with Image.open(io.BytesIO(image_bytes)) as image:
            image_format = image.format
            if image_format not in IMAGE_FORMATS:
                raise HTTPException(status_code=415, detail="Use uma imagem JPG, PNG ou WEBP.")
            if image.width * image.height > MAX_IMAGE_PIXELS:
                raise HTTPException(
                    status_code=400,
                    detail="A resolução da imagem é muito grande. Escolha uma foto menor.",
                )
            image.verify()
    except HTTPException:
        raise
    except (Image.DecompressionBombError, UnidentifiedImageError, OSError) as error:
        raise HTTPException(status_code=400, detail="O arquivo não é uma imagem válida.") from error

    return IMAGE_FORMATS[image_format]
