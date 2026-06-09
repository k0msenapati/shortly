import pytest
from httpx import AsyncClient
from datetime import datetime, timedelta, timezone
from sqlmodel import select
from database import AsyncSession
from models import URL

@pytest.mark.asyncio
async def test_url_expiration(client: AsyncClient, session: AsyncSession):
    # Manually create an expired URL in the database
    expired_url = URL(
        long_url="https://expired.com",
        short_code="expired1",
        expires_at=datetime.now(timezone.utc) - timedelta(days=1)
    )
    session.add(expired_url)
    await session.commit()
    await session.refresh(expired_url)

    # Try to redirect
    response = await client.get("/api/urls/expired1")
    assert response.status_code == 410
    assert response.json()["detail"] == "This short link has expired!"

    # Check if is_expired is true in the read schema
    analytics_response = await client.get("/api/urls/expired1/analytics")
    assert analytics_response.status_code == 200
    data = analytics_response.json()
    assert data["is_expired"] is True

@pytest.mark.asyncio
async def test_url_active(client: AsyncClient, session: AsyncSession):
    # Manually create a non-expired URL
    active_url = URL(
        long_url="https://active.com",
        short_code="active1",
        expires_at=datetime.now(timezone.utc) + timedelta(days=1)
    )
    session.add(active_url)
    await session.commit()
    await session.refresh(active_url)

    # Try to redirect
    response = await client.get("/api/urls/active1")
    assert response.status_code == 302
    assert response.headers["location"].rstrip("/") == "https://active.com"

    # Check if is_expired is false in the read schema
    analytics_response = await client.get("/api/urls/active1/analytics")
    assert analytics_response.status_code == 200
    data = analytics_response.json()
    assert data["is_expired"] is False
