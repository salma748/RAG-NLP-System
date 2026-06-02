from fastapi import APIRouter, Depends

from helpers.config import Settings, get_settings


base_router = APIRouter(prefix="/api", tags=["base"])


@base_router.get("/")
async def welcome(settings: Settings = Depends(get_settings)):
    return {
        "message": f"Welcome to the {settings.APP_NAME} App v{settings.APP_VERSION}!"
    }
