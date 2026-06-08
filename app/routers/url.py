from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database import AsyncSession, get_session
from models import URLCreate, URL, URLRead, User
from core.dependencies import get_current_user
import services.url as url_service

router = APIRouter(prefix="/urls", tags=["url"])


@router.post("/shorten")
async def create_url(
    url_create: URLCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
) -> URLRead:
    user_id = current_user.id if current_user else None
    url = await url_service.create_url(url_create, session, user_id=user_id)
    return URLRead.model_validate(url)


@router.get("/")
async def get_my_urls(
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
) -> list[URLRead]:
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    urls = await url_service.get_user_urls(current_user.id, session)
    return [URLRead.model_validate(url) for url in urls]


@router.get("/{short_code}")
async def redirect_to_original_url(
    short_code: str, session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await url_service.get_url_by_code(short_code, session)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found!")

    return RedirectResponse(str(url.long_url), 302)
