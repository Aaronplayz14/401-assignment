from fastapi.testclient import TestClient

from src.main import app


client = TestClient(app)


def test_get_items():
    response = client.get("/api/v1/items")

    if response.status_code != 200:
        raise AssertionError(
            f"Expected 200, got {response.status_code}"
        )

    body = response.json()

    if body["status"] != "ok":
        raise AssertionError("Expected status to be ok")

    if not isinstance(body["data"], list):
        raise AssertionError("Expected data to be a list")


def test_get_items_pagination_limit_5_offset_5():
    response = client.get("/api/v1/items?limit=5&offset=5")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert isinstance(body["data"], list)
    assert len(body["data"]) == 5


def test_get_items_limit_too_large_returns_400():
    response = client.get("/api/v1/items?limit=51")
    assert response.status_code == 400
    body = response.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_get_single_item_not_found():
    response = client.get("/api/v1/items/not-a-real-id")
    assert response.status_code == 404
    body = response.json()
    assert body["status"] == "error"
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["message"] == "Item not found"


def test_create_item_returns_201():
    payload = {
        "title": "Test Item",
        "source": {"name": "Test Source"},
        "publishedAt": "2025-03-10T12:00:00Z",
        "url": "https://example.com/test",
        "summary": "Test summary",
        "tags": ["test", "api"],
    }
    response = client.post("/api/v1/items", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "ok"
    assert "id" in body["data"]
    assert isinstance(body["data"]["id"], str)
    assert body["data"]["title"] == payload["title"]
