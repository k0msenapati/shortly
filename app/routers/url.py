from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database import AsyncSession, get_session
from models import URLCreate, URL
import services.url as url_service

router = APIRouter(prefix="/urls", tags=["url"])


@router.post("/shorten")
async def create_short_code(
    url_create: URLCreate, session: AsyncSession = Depends(get_session)
) -> URL:
    url = await url_service.create_url(url_create, session)
    return url


@router.get("/{short_code}")
async def redirect_to_original_url(
    short_code: str, session: AsyncSession = Depends(get_session)
) -> RedirectResponse:
    url = await url_service.get_url_by_code(short_code, session)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found!")

    return RedirectResponse(str(url.long_url), 302)
