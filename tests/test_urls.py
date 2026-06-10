import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_url_guest(client: AsyncClient):
    response = await client.post(
        "/api/urls/shorten", json={"long_url": "https://google.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://google.com/"
    assert "short_code" in data


@pytest.mark.asyncio
async def test_create_url_authenticated(client: AsyncClient, auth_headers: dict):
    response = await client.post(
        "/api/urls/shorten",
        json={"long_url": "https://github.com"},
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["long_url"] == "https://github.com/"

    # Check if URL appears in user's list
    list_response = await client.get("/api/urls/", headers=auth_headers)
    assert list_response.status_code == 200
    assert any(url["short_code"] == data["short_code"] for url in list_response.json())


@pytest.mark.asyncio
async def test_redirect_url(client: AsyncClient):
    # Create one
    create_res = await client.post(
        "/api/urls/shorten", json={"long_url": "https://example.com"}
    )
    short_code = create_res.json()["short_code"]

    # Redirect
    # Note: We use follow_redirects=False to check the 302 status
    response = await client.get(f"/api/urls/{short_code}")
    assert response.status_code == 302
    assert response.headers["location"] == "https://example.com/"


@pytest.mark.asyncio
async def test_redirect_not_found(client: AsyncClient):
    response = await client.get("/api/urls/nonexistent")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_my_urls_unauthorized(client: AsyncClient):
    response = await client.get("/api/urls/")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_search_urls_unauthorized(client: AsyncClient):
    response = await client.get("/api/urls/search?q=test")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_search_urls_success(client: AsyncClient, auth_headers: dict):
    # 1. Create a few urls
    await client.post(
        "/api/urls/shorten",
        json={"long_url": "https://github.com/fastapi/fastapi"},
        headers=auth_headers,
    )
    await client.post(
        "/api/urls/shorten",
        json={"long_url": "https://google.com"},
        headers=auth_headers,
    )
    await client.post(
        "/api/urls/shorten",
        json={"long_url": "https://github.com/tiangolo/sqlmodel"},
        headers=auth_headers,
    )

    # 2. Search for "github"
    res1 = await client.get("/api/urls/search?q=github", headers=auth_headers)
    assert res1.status_code == 200
    urls1 = res1.json()
    assert len(urls1) == 2
    assert all("github" in url["long_url"] for url in urls1)

    # 3. Search for "google"
    res2 = await client.get("/api/urls/search?q=google", headers=auth_headers)
    assert res2.status_code == 200
    urls2 = res2.json()
    assert len(urls2) == 1
    assert urls2[0]["long_url"] == "https://google.com/"

    # 4. Search with empty query
    res3 = await client.get("/api/urls/search", headers=auth_headers)
    assert res3.status_code == 200
    urls3 = res3.json()
    # At least 3 urls should exist in total
    assert len(urls3) >= 3


@pytest.mark.asyncio
async def test_reactivate_url_success(client: AsyncClient, auth_headers: dict):
    # 1. Create an expired URL (expires 1 hour ago)
    from datetime import datetime, timedelta, timezone
    past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    
    create_res = await client.post(
        "/api/urls/shorten",
        json={"long_url": "https://expired.com", "expires_at": past_time},
        headers=auth_headers,
    )
    assert create_res.status_code == 200
    short_code = create_res.json()["short_code"]
    assert create_res.json()["is_expired"] is True

    # 2. Reactivate with no expiration
    reactivate_res = await client.post(
        f"/api/urls/{short_code}/reactivate",
        json={"expires_at": None},
        headers=auth_headers,
    )
    assert reactivate_res.status_code == 200
    data = reactivate_res.json()
    assert data["expires_at"] is None
    assert data["is_expired"] is False

    # 3. Reactivate with a future expiration date
    future_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    reactivate_res = await client.post(
        f"/api/urls/{short_code}/reactivate",
        json={"expires_at": future_time},
        headers=auth_headers,
    )
    assert reactivate_res.status_code == 200
    data = reactivate_res.json()
    assert data["is_expired"] is False
    assert data["expires_at"] is not None


@pytest.mark.asyncio
async def test_reactivate_url_unauthorized(client: AsyncClient):
    response = await client.post("/api/urls/somecode/reactivate", json={})
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_deactivate_url_success(client: AsyncClient, auth_headers: dict):
    # 1. Create an active URL
    create_res = await client.post(
        "/api/urls/shorten",
        json={"long_url": "https://active-to-deactive.com"},
        headers=auth_headers,
    )
    assert create_res.status_code == 200
    short_code = create_res.json()["short_code"]
    assert create_res.json()["is_expired"] is False

    # 2. Deactivate it
    deactivate_res = await client.post(
        f"/api/urls/{short_code}/deactivate",
        headers=auth_headers,
    )
    assert deactivate_res.status_code == 200
    data = deactivate_res.json()
    assert data["is_expired"] is True
    assert data["expires_at"] is not None


@pytest.mark.asyncio
async def test_deactivate_url_unauthorized(client: AsyncClient):
    response = await client.post("/api/urls/somecode/deactivate")
    assert response.status_code == 401



