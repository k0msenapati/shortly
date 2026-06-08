from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import User, UserCreate
from utils.security import (
    hash_password,
    verify_password,
    create_access_token,
)


async def register(
    user_create: UserCreate,
    session: AsyncSession,
) -> User:
    stmt = select(User).where(User.email == user_create.email)
    res = await session.execute(stmt)
    existing = res.scalar_one_or_none()

    if existing:
        raise ValueError("Email already exists")

    user = User(
        full_name=user_create.full_name,
        user_name=user_create.user_name,
        email=user_create.email,
        hashed_password=hash_password(user_create.password),
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


async def login(
    email: str,
    password: str,
    session: AsyncSession,
) -> str:
    stmt = select(User).where(User.email == email)
    res = await session.execute(stmt)
    user = res.scalar_one_or_none()

    if not user:
        raise ValueError("Invalid credentials")

    if not verify_password(
        password,
        user.hashed_password,
    ):
        raise ValueError("Invalid credentials")

    assert user.id is not None

    return create_access_token(user.id)
