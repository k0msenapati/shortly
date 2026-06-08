from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from models import User, UserUpdate
from utils.security import hash_password


async def get_user_by_id(user_id: int, session: AsyncSession) -> User | None:
    return await session.get(User, user_id)


async def update_user(
    user_id: int, user_update: UserUpdate, session: AsyncSession
) -> User | None:
    user = await session.get(User, user_id)
    if not user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)

    if "password" in update_data:
        password = update_data.pop("password")
        if password:
            user.hashed_password = hash_password(password)

    for key, value in update_data.items():
        setattr(user, key, value)

    await session.commit()
    await session.refresh(user)

    return user
