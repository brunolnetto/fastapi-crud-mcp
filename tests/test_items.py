import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.server.main import app
from backend.server.db import get_db
from backend.server.models import Base

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: clear data before each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # Teardown: clear data after each test
    Base.metadata.drop_all(bind=engine)


def test_create_item():
    response = client.post("/api/items/", json={"name": "Test Item", "description": "A test item"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "A test item"
    assert "id" in data

def test_read_item():
    # First, create an item
    response = client.post("/api/items/", json={"name": "Read Item", "description": "Read description"})
    item_id = response.json()["id"]

    # Now, read the item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "Read Item"
    assert data["description"] == "Read description"

def test_read_items():
    # Create multiple items
    client.post("/api/items/", json={"name": "Item 1", "description": "Desc 1"})
    client.post("/api/items/", json={"name": "Item 2", "description": "Desc 2"})

    response = client.get("/api/items/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2

def test_update_item():
    # Create an item
    response = client.post("/api/items/", json={"name": "Old Name", "description": "Old description"})
    item_id = response.json()["id"]

    # Update the item
    response = client.put(f"/api/items/{item_id}", json={"name": "New Name", "description": "New description"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == "New Name"
    assert data["description"] == "New description"

def test_delete_item():
    # Create an item
    response = client.post("/api/items/", json={"name": "To Delete", "description": "To be deleted"})
    item_id = response.json()["id"]

    # Delete the item
    response = client.delete(f"/api/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True

    # Try to get the deleted item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 404

def test_update_nonexistent_item():
    non_existent_id = 9999  # Assuming this ID does not exist in the test database
    update_data = {"name": "Updated Name", "description": "Updated Description"}
    response = client.put(f"/api/items/{non_existent_id}", json=update_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}

def test_delete_nonexistent_item():
    non_existent_id = 9999  # Assuming this ID does not exist in the test database
    response = client.delete(f"/api/items/{non_existent_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
