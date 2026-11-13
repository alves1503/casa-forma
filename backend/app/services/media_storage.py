import re
from pathlib import PurePosixPath

from fastapi import HTTPException

from ..config import Settings

MEDIA_FILENAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*\.(?:jpg|png|webp)$")


def resolve_media_path(settings: Settings, photo_path: str):
    path = PurePosixPath(photo_path)
    if (
        len(path.parts) != 2
        or path.parts[0] not in {"demo", "uploads"}
        or not MEDIA_FILENAME.fullmatch(path.parts[1])
    ):
        raise HTTPException(status_code=404, detail="Imagem não encontrada.")

    directory = (
        settings.demo_image_directory
        if path.parts[0] == "demo"
        else settings.upload_directory
    )
    file_path = directory / path.parts[1]
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Imagem não encontrada.")
    return file_path
