from fastapi import APIRouter
from routes.base import base_router

router = APIRouter()
router.include_router(base_router)

_all_ = ["router"]