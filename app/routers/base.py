from fastapi import APIRouter

from routers.url import router as url_router

router = APIRouter(prefix="/api")

router.include_router(url_router)
