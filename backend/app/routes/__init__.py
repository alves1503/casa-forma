from .admin_routes import router as admin_router
from .catalog_routes import router as catalog_router
from .preview_routes import router as preview_router

all_routers = [catalog_router, preview_router, admin_router]
