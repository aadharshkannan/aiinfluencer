from db import Base, models, schemas
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def test_video_model_roundtrip():
    engine = create_engine("sqlite:///:memory:")
    TestingSession = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSession()

    video = models.Video(proverb="test", story="s", screenplay="sc", status="done")
    session.add(video)
    session.commit()

    retrieved = session.query(models.Video).first()
    assert retrieved is not None
    assert retrieved.proverb == "test"

    schema_obj = schemas.Video.from_orm(retrieved)
    assert schema_obj.id == retrieved.id
    assert schema_obj.status == "done"

