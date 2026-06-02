from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_item():
    response = client.post(
        "/items/",
        json={
            "name": "Laptop",
            "description": "MacBook Pro"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Laptop"


def test_get_items():
    response = client.get("/items/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_item():
    create = client.post(
        "/items/",
        json={
            "name": "Phone",
            "description": "Android"
        }
    )

    item_id = create.json()["id"]

    response = client.get(f"/items/{item_id}")

    assert response.status_code == 200
    assert response.json()["id"] == item_id


def test_update_item():
    create = client.post(
        "/items/",
        json={
            "name": "Old",
            "description": "Old desc"
        }
    )

    item_id = create.json()["id"]

    response = client.put(
        f"/items/{item_id}",
        json={
            "name": "New",
            "description": "New desc"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "New"


def test_delete_item():
    create = client.post(
        "/items/",
        json={
            "name": "Delete Me",
            "description": "Temp"
        }
    )

    item_id = create.json()["id"]

    response = client.delete(
        f"/items/{item_id}"
    )

    assert response.status_code == 200