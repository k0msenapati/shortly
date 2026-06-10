from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from database import AsyncSession, get_session
from models import URLCreate, URL, URLRead, User, URLReactivate
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
    assert current_user.id is not None
    urls = await url_service.get_user_urls(current_user.id, session)
    return [URLRead.model_validate(url) for url in urls]


@router.get("/search")
async def search_urls(
    q: str = "",
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
) -> list[URLRead]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    assert current_user.id is not None

    urls = await url_service.search_user_urls_by_long_url(current_user.id, q, session)
    return [URLRead.model_validate(url) for url in urls]


@router.get("/{short_code}")
async def redirect_to_original_url(
    short_code: str,
    src: str | None = None,
    session: AsyncSession = Depends(get_session),
) -> RedirectResponse:
    url = await url_service.get_url_by_code(short_code, session)

    if not url:
        raise HTTPException(status_code=404, detail="URL not found!")

    url = URLRead.model_validate(url)

    if url.is_expired:
        raise HTTPException(status_code=410, detail="This short link has expired!")

    await url_service.increment_clicks(url.id, src == "qr", session)

    return RedirectResponse(str(url.long_url), 302)


@router.get("/{short_code}/analytics")
async def get_url_analytics(
    short_code: str,
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
) -> URLRead:
    url = await url_service.get_url_by_code(short_code, session)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found!")

    if url.user_id and (not current_user or current_user.id != url.user_id):
        raise HTTPException(status_code=403, detail="Forbidden")

    return URLRead.model_validate(url)


@router.post("/{short_code}/reactivate")
async def reactivate_url(
    short_code: str,
    reactivate_data: URLReactivate | None = None,
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
) -> URLRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    url = await url_service.get_url_by_code(short_code, session)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found!")

    if url.user_id and url.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    expires_at = reactivate_data.expires_at if reactivate_data else None
    updated_url = await url_service.reactivate_url(url.id, expires_at, session) # type: ignore
    return URLRead.model_validate(updated_url)


@router.post("/{short_code}/deactivate")
async def deactivate_url(
    short_code: str,
    session: AsyncSession = Depends(get_session),
    current_user: User | None = Depends(get_current_user),
) -> URLRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    url = await url_service.get_url_by_code(short_code, session)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found!")

    if url.user_id and url.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    from datetime import datetime, timezone
    updated_url = await url_service.deactivate_url(url.id, datetime.now(timezone.utc), session) # type: ignore
    return URLRead.model_validate(updated_url)

