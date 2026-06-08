from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import User, UserRead, UserUpdate
from core.dependencies import get_current_user
import services.user as user_service

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )
    return UserRead.model_validate(current_user)


@router.patch("/me")
async def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    if not current_user:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated",
        )

    user = await user_service.update_user(current_user.id, user_update, session)
    return UserRead.model_validate(user)


@router.get("/{user_id}")
async def get_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await user_service.get_user_by_id(user_id, session)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return UserRead.model_validate(user)
