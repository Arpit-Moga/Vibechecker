import io
import pytest
from fastapi.testclient import TestClient
from mcp_server.server import app

client = TestClient(app)

# Helper to create a dummy file of given size
def make_file(size):
    return io.BytesIO(b'a' * size)

def test_upload_codebase_valid():
    response = client.post("/upload_codebase", files={"codebase": ("test.zip", make_file(1024))})
    assert response.status_code == 200
    assert response.json()["status"] == "uploaded"
    assert "id" in response.json()

def test_upload_codebase_too_large():
    response = client.post("/upload_codebase", files={"codebase": ("big.zip", make_file(501 * 1024 * 1024))})
    assert response.status_code == 413
    assert "Payload too large" in response.json()["error"]

def test_upload_codebase_missing_file():
    response = client.post("/upload_codebase", files={})
    assert response.status_code == 422  # FastAPI validation error

def test_trigger_review_valid():
    # Upload first
    upload = client.post("/upload_codebase", files={"codebase": ("test.zip", make_file(1024))})
    codebase_id = upload.json()["id"]
    response = client.post("/trigger_review", json={"id": codebase_id})
    assert response.status_code == 200 or response.status_code == 202
    assert response.json()["status"] == "review_started"
    assert "id" in response.json()

def test_trigger_review_not_found():
    response = client.post("/trigger_review", json={"id": "nonexistent"})
    assert response.status_code == 404
    assert "Codebase not found" in response.json()["error"]

def test_get_results_valid():
    # Upload and trigger review
    upload = client.post("/upload_codebase", files={"codebase": ("test.zip", make_file(1024))})
    codebase_id = upload.json()["id"]
    review = client.post("/trigger_review", json={"id": codebase_id})
    review_id = review.json()["id"]
    response = client.get(f"/get_results?id={review_id}")
    assert response.status_code == 200
    data = response.json()
    assert "documentation" in data
    assert "debt" in data
    assert "improvement" in data
    assert "critical" in data

def test_get_results_not_found():
    response = client.get("/get_results?id=nonexistent")
    assert response.status_code == 404
    assert "Review not found" in response.json()["error"]
