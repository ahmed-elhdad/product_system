from fastapi import APIRouter
from src.config import get_settings, Settings

base_router = APIRouter(prefix="/api/v1", tags=["api_v1"])


@base_router.get("/health")
async def Health(app_settings: Settings = get_settings()):
    return {"app_name": app_settings.APP_NAME, "app_version": app_settings.APP_VERSION}
