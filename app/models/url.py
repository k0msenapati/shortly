from typing import TYPE_CHECKING, Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import HttpUrl
from datetime import datetime, timezone

if TYPE_CHECKING:
    from .user import User


class URL(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: int | None = Field(default=None, primary_key=True)
    long_url: str
    short_code: str | None = Field(
        default=None,
        unique=True,
        index=True,
        min_length=7,
        max_length=20,
    )
    total_clicks: int = Field(default=0)
    qr_clicks: int = Field(default=0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user_id: int | None = Field(
        default=None,
        foreign_key="user.id",
    )
    user: Optional["User"] = Relationship(back_populates="urls")


# Request Schemas


class URLCreate(SQLModel):
    long_url: HttpUrl


# Response Schemas


class URLRead(SQLModel):
    id: int
    long_url: str
    short_code: str
    total_clicks: int
    qr_clicks: int
    created_at: datetime
