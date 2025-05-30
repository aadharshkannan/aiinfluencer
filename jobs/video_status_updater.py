import os
import time
import logging
import requests
from sqlalchemy.orm import Session

from db import SessionLocal, models
from utils import SynthesiaClient

logger = logging.getLogger(__name__)

def check_pending_videos(session: Session, client: SynthesiaClient) -> int:
    """Check videos marked as in_progress and update their status."""
    updated = 0
    videos = session.query(models.Video).filter(models.Video.status == "in_progress").all()
    for video in videos:
        try:
            status_model = client.get_video_status(video.id)
            status = status_model.status
            if status and status != video.status:
                video.status = status
                session.commit()
                updated += 1
                logger.info("Updated video %s status to %s", video.id, status)
        except requests.RequestException as exc:
            session.rollback()
            logger.error("Failed to fetch status for %s: %s", video.id, exc)
    return updated


def run_forever() -> None:
    client = SynthesiaClient()
    interval = int(os.getenv("VIDEO_STATUS_CHECK_INTERVAL", "60"))
    while True:
        session = SessionLocal()
        try:
            check_pending_videos(session, client)
        finally:
            session.close()
        time.sleep(interval)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_forever()