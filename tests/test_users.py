import pytest
from httpx import AsyncClient
from models import User


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, auth_headers: dict):
    response = await client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    response = await client.get("/api/users/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_me(client: AsyncClient, auth_headers: dict):
    response = await client.patch(
        "/api/users/me",
        headers=auth_headers,
        json={"full_name": "Updated Name", "password": "newpassword123"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

    # Verify login with new password
    login_response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "newpassword123"},
    )
    assert login_response.status_code == 200


@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, test_user: User):
    response = await client.get(f"/api/users/{test_user.id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_user.id


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    response = await client.get("/api/users/9999")
    assert response.status_code == 404
