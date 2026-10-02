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