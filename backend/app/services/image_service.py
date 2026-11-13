import base64
import io

from openai import OpenAI, OpenAIError

IMAGE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


class ImageGenerationError(Exception):
    pass


def create_room_preview(
    room_image: bytes,
    room_content_type: str,
    furniture_image: bytes,
    furniture_content_type: str,
    furniture: dict,
    api_key: str | None,
    model: str,
):
    if not api_key:
        raise ImageGenerationError(
            "A chave da OpenAI não está configurada. Defina OPENAI_API_KEY no ambiente do servidor."
        )

    prompt = (
        "There are two input images. The first is the customer's room; the second is a reference "
        "photo of the selected furniture. Edit the first image as a photorealistic interior design "
        "visualization. Add exactly one instance of the furniture shown in the second image, "
        f"{furniture['name']}. Treat the second image as the authoritative reference for the "
        "furniture's design, color, material, shape, and proportions; "
        "do not copy its background, room, or other objects. Place it naturally in a suitable, "
        "unoccupied area of the customer's room, at realistic scale and perspective. Match the "
        "room's existing lighting, shadows, camera angle, and color balance. Keep the existing room "
        "architecture and furnishings unchanged."
    )

    try:
        response = OpenAI(api_key=api_key).images.edit(
            model=model,
            image=[
                (
                    f"room{IMAGE_EXTENSIONS[room_content_type]}",
                    io.BytesIO(room_image),
                    room_content_type,
                ),
                (
                    f"furniture-reference{IMAGE_EXTENSIONS[furniture_content_type]}",
                    io.BytesIO(furniture_image),
                    furniture_content_type,
                ),
            ],
            prompt=prompt,
            quality="low",
            size="auto",
            output_format="png",
        )
    except OpenAIError as error:
        raise ImageGenerationError(
            "Não foi possível gerar a prévia. Verifique a chave, o acesso ao modelo e tente novamente."
        ) from error

    if not response.data or not response.data[0].b64_json:
        raise ImageGenerationError("O serviço não retornou uma imagem. Tente novamente.")

    return base64.b64decode(response.data[0].b64_json)
