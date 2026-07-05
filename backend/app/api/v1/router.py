from fastapi import APIRouter
from app.api.v1.routers import health

api_router = APIRouter()

# Register core application routers
api_router.include_router(health.router, prefix="/health", tags=["system-health"])

# Placeholder routers for future development:
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# api_router.include_router(incidents.router, prefix="/incidents", tags=["incidents"])
# api_router.include_router(investigation.router, prefix="/investigation", tags=["investigation"])
# api_router.include_router(reporting.router, prefix="/reporting", tags=["reporting"])
# api_router.include_router(rag.router, prefix="/rag", tags=["rag"])
