from fastapi import APIRouter

from routers.url import router as url_router
from routers.auth import router as auth_router
from routers.user import router as user_router

router = APIRouter(prefix="/api")

router.include_router(url_router)
router.include_router(auth_router)
router.include_router(user_router)
