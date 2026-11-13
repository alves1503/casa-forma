from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import FileResponse

from .config import PROJECT_DIR, Settings
from .routes import all_routers
from .seed import seed_database

__all__ = ["app", "create_app"]


def create_app(settings: Settings | None = None):
    app_settings = settings or Settings.from_environment()

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        seed_database(app_settings)
        app_settings.upload_directory.mkdir(parents=True, exist_ok=True)
        yield

    application = FastAPI(
        title="Casa Forma API",
        version="1.0.0",
        docs_url=None,
        redoc_url=None,
        openapi_url=None,
        lifespan=lifespan,
    )
    application.state.settings = app_settings
    application.add_middleware(
        CORSMiddleware,
        allow_origins=list(app_settings.allowed_origins),
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    for router in all_routers:
        application.include_router(router)

    @application.get("/api/health")
    def health():
        return {"status": "ok"}

    @application.get("/docs", include_in_schema=False)
    def swagger_ui():
        return get_swagger_ui_html(
            openapi_url="/openapi.yaml",
            title=f"{application.title} - Swagger UI",
        )

    @application.get("/openapi.yaml", include_in_schema=False)
    def openapi_yaml():
        return FileResponse(
            PROJECT_DIR / "docs" / "openapi.yaml",
            media_type="application/yaml",
        )

    return application


app = create_app()
