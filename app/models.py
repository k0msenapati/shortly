from sqlmodel import SQLModel, Field
from pydantic import HttpUrl
from datetime import datetime, timezone


class URL(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    long_url: str
    short_code: str | None = Field(default=None, min_length=7)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc), nullable=False
    )


class URLCreate(SQLModel):
    long_url: HttpUrl
