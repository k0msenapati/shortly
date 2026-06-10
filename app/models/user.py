from typing import TYPE_CHECKING, List

from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import DateTime
from pydantic import EmailStr
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .url import URL


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    full_name: str | None = None
    user_name: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    hashed_password: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_type=DateTime(timezone=True),  # type: ignore
        nullable=False,
    )

    urls: List["URL"] = Relationship(back_populates="user")


# Request Schemas


class UserCreate(SQLModel):
    full_name: str | None = None
    user_name: str
    email: EmailStr
    password: str


class UserLogin(SQLModel):
    email: EmailStr
    password: str


class UserUpdate(SQLModel):
    full_name: str | None = None
    user_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None


# Response Schemas


class UserRead(SQLModel):
    id: int
    full_name: str | None
    user_name: str
    email: EmailStr
    created_at: datetime


# Auth Schemas


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
