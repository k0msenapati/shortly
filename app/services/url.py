from sqlmodel import select, update
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from models import URL, URLCreate
from utils.shortener import generate_short_code


async def create_url(
    url_create: URLCreate, session: AsyncSession, user_id: int | None = None
) -> URL:
    url = URL(
        long_url=str(url_create.long_url),
        user_id=user_id,
        expires_at=url_create.expires_at,
    )

    session.add(url)
    await session.flush()

    assert url.id is not None
    url.short_code = generate_short_code(url.id)

    session.add(url)
    await session.commit()
    await session.refresh(url)

    return url


async def get_url_by_code(short_code: str, session: AsyncSession) -> URL | None:
    stmt = select(URL).where(URL.short_code == short_code)
    res = await session.execute(stmt)

    return res.scalar_one_or_none()


async def get_user_urls(user_id: int, session: AsyncSession) -> list[URL]:
    stmt = select(URL).where(URL.user_id == user_id)
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def increment_clicks(id: int, qr: bool, session: AsyncSession):
    stmt = (
        update(URL)
        .where(URL.id == id)  # type: ignore
        .values(
            total_clicks=URL.total_clicks + 1,
            qr_clicks=URL.qr_clicks + (1 if qr else 0),
        )
    )

    await session.execute(stmt)
    await session.commit()


async def search_user_urls_by_long_url(
    user_id: int, query: str, session: AsyncSession
) -> list[URL]:
    stmt = select(URL).where(URL.user_id == user_id).where(URL.long_url.contains(query))  # type: ignore
    res = await session.execute(stmt)
    return list(res.scalars().all())


async def reactivate_url(
    id: int, expires_at: datetime | None, session: AsyncSession
) -> URL:
    stmt = update(URL).where(URL.id == id).values(expires_at=expires_at)  # type: ignore
    await session.execute(stmt)
    await session.commit()

    stmt_select = select(URL).where(URL.id == id)
    res = await session.execute(stmt_select)
    return res.scalar_one()


async def deactivate_url(
    id: int, deactivated_at: datetime, session: AsyncSession
) -> URL:
    stmt = (
        update(URL)
        .where(URL.id == id)  # type: ignore
        .values(expires_at=deactivated_at)
    )
    await session.execute(stmt)
    await session.commit()

    stmt_select = select(URL).where(URL.id == id)
    res = await session.execute(stmt_select)
    return res.scalar_one()
