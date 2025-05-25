from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Video(Base):
    """SQLAlchemy model for generated videos."""

    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    proverb: Mapped[str] = mapped_column(String, nullable=False)
    story: Mapped[str | None] = mapped_column(Text, nullable=True)
    screenplay: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String, default="pending", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

