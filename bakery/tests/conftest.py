# tests/conftest.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base

# Use a different database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="function")
def test_engine():
    # Create an SQLite engine for testing
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    return engine


@pytest.fixture(scope="function")
def setup_database(test_engine):
    # Create all tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Drop all tables after the test is done
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db_session(test_engine, setup_database):
    SessionLocal = sessionmaker(bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()
