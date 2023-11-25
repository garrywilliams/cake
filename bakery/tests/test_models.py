# tests/test_models.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Cake

# Setup in-memory SQLite for testing
engine = create_engine("sqlite:///:memory:", echo=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def test_create_cake():
    db = TestingSessionLocal()
    new_cake = Cake(
        name="Test Cake",
        comment="Delicious cake",
        imageUrl="http://example.com/cake.jpg",
        yumFactor=3,
    )
    db.add(new_cake)
    db.commit()
    assert new_cake.id is not None


def test_cake_name_length_too_long():
    with pytest.raises(ValueError):
        Cake(
            name="x" * 31,
            comment="Test comment",
            imageUrl="http://example.com/cake.jpg",
            yumFactor=3,
        )


def test_cake_name_length_too_short():
    with pytest.raises(ValueError):
        Cake(
            name="x" * 4,
            comment="Test comment",
            imageUrl="http://example.com/cake.jpg",
            yumFactor=3,
        )


def test_cake_comment_length_too_long():
    with pytest.raises(ValueError):
        Cake(
            name="Test Cake",
            comment="x" * 201,
            imageUrl="http://example.com/cake.jpg",
            yumFactor=3,
        )


def test_cake_comment_length_too_short():
    with pytest.raises(ValueError):
        Cake(
            name="Test Cake",
            comment="x" * 4,
            imageUrl="http://example.com/cake.jpg",
            yumFactor=3,
        )


def test_yum_factor_range():
    with pytest.raises(ValueError):
        Cake(
            name="Test Cake",
            comment="Test comment",
            imageUrl="http://example.com/cake.jpg",
            yumFactor=6,
        )
