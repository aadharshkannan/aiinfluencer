from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch

from db import Base, models
from jobs.video_status_updater import check_pending_videos
from utils import SynthesiaClient


def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSession


@patch.object(SynthesiaClient, "get_video_status")
def test_check_pending_videos_updates_status(mock_get_status):
    engine, TestingSession = setup_in_memory_db()
    session = TestingSession()

    video = models.Video(
        id="vid1",
        proverb="p",
        story=None,
        screenplay=None,
        status="in_progress",
    )
    session.add(video)
    session.commit()

    from utils import VideoStatus

    mock_get_status.return_value = VideoStatus(id="vid1", status="complete")

    client = SynthesiaClient(api_key="fake")
    updated = check_pending_videos(session, client)

    assert updated == 1
    session.refresh(video)
    assert video.status == "complete"