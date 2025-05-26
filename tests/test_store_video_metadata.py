from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, models
from db.utils import store_video_metadata


def test_store_video_metadata_inserts_row():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSession()

    resp = {
        "id": "uuid-123",
        "description": "desc",
        "status": "in_progress",
        "createdAt": 1_700_000_000,
    }

    store_video_metadata(session, "prov", "story", "screenplay", resp)

    saved = session.query(models.Video).first()
    assert saved is not None
    assert saved.proverb == "prov"
    assert saved.story == "story"
    assert saved.screenplay == "screenplay"
    assert saved.status == "in_progress"
    assert saved.created_at == datetime.fromtimestamp(resp["createdAt"])
