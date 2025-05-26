from __future__ import annotations

from datetime import datetime
import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from .models import Video

logger = logging.getLogger(__name__)


def store_video_metadata(
    session: Session,
    proverb: str,
    story: str | None,
    screenplay: str | None,
    video_response: dict,
) -> int:
    """Persist Synthesia video metadata to the database.

    Parameters
    ----------
    session:
        SQLAlchemy session used for the insert.
    proverb:
        The proverb that inspired the video.
    story:
        Generated story text.
    screenplay:
        Generated screenplay text (used as video script).
    video_response:
        JSON dictionary returned by Synthesia's API.

    Returns
    -------
    int
        The auto-generated database ID of the inserted ``Video`` row.
    """

    created_ts = video_response.get("createdAt")
    created_at = (
        datetime.fromtimestamp(created_ts) if isinstance(created_ts, (int, float)) else datetime.utcnow()
    )
    status = video_response.get("status", "unknown")
    synthesia_id = video_response.get("id")

    video = Video(
        id = synthesia_id,
        proverb=proverb,
        story=story,
        screenplay=screenplay,
        status=status,
        created_at=created_at,
    )

    try:
        session.add(video)
        session.commit()
    except SQLAlchemyError as exc:  # pragma: no cover - tested via exception path
        session.rollback()
        raise RuntimeError("Failed to store video metadata") from exc

    logger.info("Stored Synthesia video %s as DB record %s", synthesia_id, video.id)
    return video.id
