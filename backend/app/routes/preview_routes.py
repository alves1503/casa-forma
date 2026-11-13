from fastapi import APIRouter, File, Form, Request, UploadFile

from ..controllers import preview_controller
from ..views.preview import PreviewView

router = APIRouter()


@router.post("/api/preview", response_model=PreviewView)
async def generate_preview(
    request: Request,
    room_photo: UploadFile = File(...),
    furniture_id: str = Form(...),
):
    return await preview_controller.generate_preview(
        request.app.state.settings,
        room_photo,
        furniture_id,
    )
