from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel, ConfigDict

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

    model_config = ConfigDict(from_attributes=True)
