from sqlalchemy.orm import Session

from app.main import get_db


def test_get_db():
    generator = get_db()
    db = next(generator)
    try:
        assert isinstance(db, Session)
    finally:
        # It's important to ensure the generator is properly exhausted
        # to trigger the cleanup code (db.close() in this case).
        next(generator, None)
