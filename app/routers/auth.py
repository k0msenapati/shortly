from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import (
    UserCreate,
    UserLogin,
    UserRead,
    Token,
    User,
)
from core.dependencies import get_current_user
import services.auth as auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    status_code=201,
)
async def register(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    try:
        user_read = await auth_service.register(user_create, session)
        return UserRead.model_validate(user_read)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post(
    "/login",
)
async def login(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_session),
) -> Token:
    try:
        access_token = await auth_service.login(
            session=session,
            email=user_login.email,
            password=user_login.password,
        )

        return Token(
            access_token=access_token,
        )

    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )
