from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel

class VideoBase(BaseModel):
    proverb: str
    story: str | None = None
    screenplay: str | None = None
    status: str = "pending"

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
