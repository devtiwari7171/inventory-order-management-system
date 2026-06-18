"""Product API tests."""
from fastapi.testclient import TestClient


def test_create_product_success(client: TestClient) -> None:
    payload = {
        "name": "Mechanical Keyboard",
        "sku": "KB-001",
        "price": 99.99,
        "stock_quantity": 25,
    }
    res = client.post("/api/v1/products/", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == payload["name"]
    assert data["sku"] == payload["sku"]
    assert float(data["price"]) == payload["price"]
    assert data["stock_quantity"] == 25


def test_create_product_duplicate_sku_returns_409(client: TestClient) -> None:
    payload = {"name": "Mouse", "sku": "M-1", "price": 10.0, "stock_quantity": 5}
    client.post("/api/v1/products/", json=payload)
    res = client.post("/api/v1/products/", json=payload)
    assert res.status_code == 409


def test_create_product_negative_price_rejected(client: TestClient) -> None:
    payload = {"name": "X", "sku": "X-1", "price": -1.0, "stock_quantity": 1}
    res = client.post("/api/v1/products/", json=payload)
    assert res.status_code == 422


def test_create_product_negative_stock_rejected(client: TestClient) -> None:
    payload = {"name": "X", "sku": "X-2", "price": 1.0, "stock_quantity": -5}
    res = client.post("/api/v1/products/", json=payload)
    assert res.status_code == 422


def test_list_products(client: TestClient) -> None:
    for i in range(3):
        client.post(
            "/api/v1/products/",
            json={"name": f"P{i}", "sku": f"SKU-{i}", "price": 1.0, "stock_quantity": 1},
        )
    res = client.get("/api/v1/products/")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


def test_search_products(client: TestClient) -> None:
    client.post("/api/v1/products/", json={"name": "Apple", "sku": "A-1", "price": 1.0, "stock_quantity": 1})
    client.post("/api/v1/products/", json={"name": "Banana", "sku": "B-1", "price": 1.0, "stock_quantity": 1})
    res = client.get("/api/v1/products/", params={"q": "App"})
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Apple"


def test_get_product_by_id(client: TestClient) -> None:
    created = client.post(
        "/api/v1/products/",
        json={"name": "Pen", "sku": "PEN-1", "price": 2.5, "stock_quantity": 100},
    ).json()
    res = client.get(f"/api/v1/products/{created['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == created["id"]


def test_get_product_not_found(client: TestClient) -> None:
    res = client.get("/api/v1/products/999")
    assert res.status_code == 404


def test_update_product(client: TestClient) -> None:
    created = client.post(
        "/api/v1/products/",
        json={"name": "Old", "sku": "OLD-1", "price": 5.0, "stock_quantity": 3},
    ).json()
    res = client.put(
        f"/api/v1/products/{created['id']}",
        json={"name": "New", "price": 7.5},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == "New"
    assert float(data["price"]) == 7.5
    assert data["sku"] == "OLD-1"  # unchanged


def test_delete_product(client: TestClient) -> None:
    created = client.post(
        "/api/v1/products/",
        json={"name": "Trash", "sku": "TR-1", "price": 1.0, "stock_quantity": 1},
    ).json()
    res = client.delete(f"/api/v1/products/{created['id']}")
    assert res.status_code == 204
    assert client.get(f"/api/v1/products/{created['id']}").status_code == 404
