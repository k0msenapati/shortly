from sqlmodel import select

from sqlalchemy.ext.asyncio import AsyncSession
from models import URL, URLCreate
from utils.shortener import generate_short_code


async def create_url(url_create: URLCreate, session: AsyncSession) -> URL:
    url = URL(long_url=str(url_create.long_url))

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
