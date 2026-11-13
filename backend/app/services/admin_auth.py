from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from ..models.admin_repository import get_admin_user
from .password_service import verify_password

basic_auth = HTTPBasic()


def require_admin(
    request: Request,
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    settings = request.app.state.settings
    admin = get_admin_user(settings, credentials.username)
    if not admin or not verify_password(credentials.password, admin["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha inválidos.",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
