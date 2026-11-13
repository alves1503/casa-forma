from fastapi import APIRouter, Depends, File, Request, UploadFile

from ..controllers import admin_controller
from ..services.admin_auth import require_admin
from ..views.furniture import FurnitureView
from ..views.preview import AdminSessionView

router = APIRouter(
    prefix="/api/admin",
    dependencies=[Depends(require_admin)],
)


@router.get("/session", response_model=AdminSessionView)
def admin_session(username: str = Depends(require_admin)):
    return admin_controller.admin_session(username)


@router.get("/furniture", response_model=list[FurnitureView])
def admin_furniture(request: Request):
    return admin_controller.admin_furniture(request.app.state.settings)


@router.post("/furniture/{furniture_id}/photo", response_model=FurnitureView)
async def update_furniture_photo(
    furniture_id: str,
    request: Request,
    photo: UploadFile = File(...),
):
    return await admin_controller.update_furniture_photo_endpoint(
        request.app.state.settings,
        furniture_id,
        photo,
    )
