# tests/test_api.py

import pytest
from fastapi.testclient import TestClient

from app.main import app, get_db

client = TestClient(app)


@pytest.fixture
def override_get_db(db_session):
    def _override_db():
        yield db_session

    return _override_db


def test_create_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db

    response = client.post(
        "/api/cakes/",
        json={
            "name": "Test Cake",
            "comment": "A test cake",
            "imageUrl": "http://example.com/test_cake.jpg",
            "yumFactor": 3,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Cake"
    assert data["comment"] == "A test cake"
    assert "id" in data


def test_get_cakes(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    response = client.get("/api/cakes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    # First, create a cake to update
    create_response = client.post(
        "/api/cakes/",
        json={
            "name": "Old Cake",
            "comment": "Before update",
            "imageUrl": "http://example.com/old_cake.jpg",
            "yumFactor": 2,
        },
    )
    cake_id = create_response.json()["id"]

    # Now, update the cake
    update_response = client.put(
        f"/api/cakes/{cake_id}",
        json={
            "name": "Updated Cake",
            "comment": "After update",
            "imageUrl": "http://example.com/updated_cake.jpg",
            "yumFactor": 4,
        },
    )
    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["name"] == "Updated Cake"


def test_delete_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    # First, create a cake to delete
    create_response = client.post(
        "/api/cakes/",
        json={
            "name": "Delete Cake",
            "comment": "To be deleted",
            "imageUrl": "http://example.com/delete_cake.jpg",
            "yumFactor": 1,
        },
    )
    cake_id = create_response.json()["id"]

    # Now, delete the cake
    delete_response = client.delete(f"/api/cakes/{cake_id}")
    assert delete_response.status_code == 200
    # Optionally, try to fetch the deleted cake to ensure it's gone
    get_response = client.get(f"/api/cakes/{cake_id}")
    assert get_response.status_code == 404


def test_read_nonexistent_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    response = client.get(
        "/api/cakes/9999"
    )  # Assuming 9999 is an ID that doesn't exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Cake not found"}


def test_read_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    # First, create a cake to read
    create_response = client.post(
        "/api/cakes/",
        json={
            "name": "Read Cake",
            "comment": "To be read",
            "imageUrl": "http://example.com/read_cake.jpg",
            "yumFactor": 1,
        },
    )
    cake_id = create_response.json()["id"]

    # Now, read the cake
    read_response = client.get(f"/api/cakes/{cake_id}")
    assert read_response.status_code == 200
    read_data = read_response.json()
    assert read_data["name"] == "Read Cake"


def test_update_nonexistent_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    response = client.put(
        "/api/cakes/9999",
        json={
            "name": "Old Cake",
            "comment": "Before update",
            "imageUrl": "http://example.com/old_cake.jpg",
            "yumFactor": 2,
        },
    )  # Replace '...' with valid cake data
    assert response.status_code == 404
    assert response.json() == {"detail": "Cake not found"}


def test_delete_nonexistent_cake(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    response = client.delete("/api/cakes/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Cake not found"}


# test the pydantic validation
def test_create_cake_invalid_url(override_get_db):
    app.dependency_overrides[get_db] = override_get_db

    response = client.post(
        "/api/cakes/",
        json={
            "name": "Test Cake",
            "comment": "A test cake",
            "imageUrl": "example.com/test_cake.jpg",
            "yumFactor": 3,
        },
    )
    assert response.status_code == 422
    response_json = response.json()
    assert response_json["detail"][0]["loc"] == ["body", "imageUrl"]
    assert (
        response_json["detail"][0]["msg"]
        == "String should match pattern '^http[s]?://.+'"
    )
    assert response_json["detail"][0]["type"] == "string_pattern_mismatch"
