import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import SQLModel

from database import get_session
from main import app
from models import User
from utils.security import hash_password

# Use in-memory SQLite for testing
engine = create_async_engine("sqlite+aiosqlite:///:memory:")
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    await engine.dispose()


@pytest_asyncio.fixture
async def session():
    async with SessionLocal() as session:
        yield session
        # Clear tables after each test to ensure isolation
        for table in reversed(SQLModel.metadata.sorted_tables):
            await session.execute(table.delete())
        await session.commit()


@pytest_asyncio.fixture
async def client(session):
    async def _get_session():
        yield session

    app.dependency_overrides[get_session] = _get_session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(session: AsyncSession):
    user = User(
        full_name="Test User",
        user_name="testuser",
        email="test@example.com",
        hashed_password=hash_password("password123"),
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, test_user: User):
    # Login with the test_user already in DB
    res = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    return {"Authorization": f"Bearer {res.json()['access_token']}"}
