import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post(
        "/api/auth/register",
        json={
            "full_name": "New User",
            "user_name": "newuser",
            "email": "new@example.com",
            "password": "securepassword",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    user_data = {
        "user_name": "user1",
        "email": "dup@example.com",
        "password": "password",
    }
    await client.post("/api/auth/register", json=user_data)
    response = await client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    # Register first
    await client.post(
        "/api/auth/register",
        json={
            "user_name": "loginuser",
            "email": "login@example.com",
            "password": "password123",
        },
    )
    # Login
    response = await client.post(
        "/api/auth/login",
        json={"email": "login@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    response = await client.post(
        "/api/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
