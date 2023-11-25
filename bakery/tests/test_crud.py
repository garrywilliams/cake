# tests/test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import crud
from app.models import Base

# Test database URL (use an in-memory SQLite database for testing)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def db_session():
    # Create an in-memory SQLite database for testing
    engine = create_engine(TEST_DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()


def test_create_cake_valid_data(db_session: Session):
    cake_data = {
        "name": "Test Cake",
        "comment": "Delicious",
        "imageUrl": "http://example.com/cake.jpg",
        "yumFactor": 4,
    }
    cake = crud.create_cake(db_session, cake_data)
    assert cake.id is not None
    assert cake.name == cake_data["name"]
    assert cake.comment == cake_data["comment"]
    assert cake.imageUrl == cake_data["imageUrl"]
    assert cake.yumFactor == cake_data["yumFactor"]


def test_create_cake_invalid_data(db_session: Session):
    invalid_cake_data = {
        "name": "x" * 35,
        "comment": "Too long name",
        "imageUrl": "http://example.com/cake.jpg",
        "yumFactor": 6,
    }
    with pytest.raises(ValueError):
        crud.create_cake(db_session, invalid_cake_data)


def test_get_cake(db_session: Session):
    cake_data = {
        "name": "Sample Cake",
        "comment": "Tasty",
        "imageUrl": "http://example.com/sample_cake.jpg",
        "yumFactor": 3,
    }
    cake = crud.create_cake(db_session, cake_data)
    retrieved_cake = crud.get_cake(db_session, cake.id)
    assert retrieved_cake.id == cake.id
    assert retrieved_cake.name == cake.name
    assert retrieved_cake.comment == cake.comment


def test_get_cakes(db_session: Session):
    # Assuming there are already some cakes in the database
    cakes = crud.get_cakes(db_session, skip=0, limit=2)
    assert len(cakes) <= 2


def test_update_cake(db_session: Session):
    cake_data = {
        "name": "Update Cake",
        "comment": "Before update",
        "imageUrl": "http://example.com/update_cake.jpg",
        "yumFactor": 4,
    }
    cake = crud.create_cake(db_session, cake_data)
    updated_data = {
        "name": "Updated Cake",
        "comment": "After update",
        "imageUrl": "http://example.com/updated_cake.jpg",
        "yumFactor": 5,
    }
    updated_cake = crud.update_cake(db_session, cake.id, updated_data)
    assert updated_cake.id == cake.id
    assert updated_cake.name == updated_data["name"]
    assert updated_cake.comment == updated_data["comment"]
    assert updated_cake.imageUrl == updated_data["imageUrl"]
    assert updated_cake.yumFactor == updated_data["yumFactor"]


def test_update_non_existent_cake(db_session: Session):
    non_existent_cake_id = 999  # An ID assumed not to exist
    updated_data = {
        "name": "Non-Existent Cake",
        "comment": "No update",
        "imageUrl": "http://example.com/non_existent.jpg",
        "yumFactor": 3,
    }
    result = crud.update_cake(db_session, non_existent_cake_id, updated_data)
    assert result is None  # Assert that None is returned for a non-existent cake


def test_delete_cake(db_session: Session):
    cake_data = {
        "name": "Delete Cake",
        "comment": "To be deleted",
        "imageUrl": "http://example.com/delete_cake.jpg",
        "yumFactor": 2,
    }
    cake = crud.create_cake(db_session, cake_data)
    crud.delete_cake(db_session, cake.id)
    deleted_cake = crud.get_cake(db_session, cake.id)
    assert deleted_cake is None
