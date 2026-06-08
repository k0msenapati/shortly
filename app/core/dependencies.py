from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from utils.security import decode_access_token
from database import get_session
from models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login", auto_error=False)


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User | None:
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        user_id = int(payload["sub"])
    except Exception:
        return None

    user = await session.get(User, user_id)

    return user
