import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_check():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "dependencies" in data


def test_extract_invalid_file_type():
    """Test PDF extraction with invalid file type."""
    files = {
        "file": ("test.txt", b"test content", "text/plain")
    }
    response = client.post("/api/v1/extract", files=files)
    assert response.status_code == 400
    assert "Invalid file type" in response.json()["detail"]


def test_extract_no_file():
    """Test PDF extraction without file."""
    response = client.post("/api/v1/extract")
    assert response.status_code == 422  # Validation error 