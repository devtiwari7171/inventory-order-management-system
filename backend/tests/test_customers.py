"""Customer API tests."""
from fastapi.testclient import TestClient


def test_create_customer_success(client: TestClient) -> None:
    payload = {"name": "Alice", "email": "alice@example.com", "phone": "555-1234"}
    res = client.post("/api/v1/customers/", json=payload)
    assert res.status_code == 201
    assert res.json()["email"] == payload["email"]


def test_create_customer_invalid_email(client: TestClient) -> None:
    payload = {"name": "Bob", "email": "not-an-email"}
    res = client.post("/api/v1/customers/", json=payload)
    assert res.status_code == 422


def test_create_customer_duplicate_email(client: TestClient) -> None:
    payload = {"name": "A", "email": "dup@example.com"}
    client.post("/api/v1/customers/", json=payload)
    res = client.post("/api/v1/customers/", json=payload)
    assert res.status_code == 409


def test_list_customers(client: TestClient) -> None:
    for i in range(2):
        client.post(
            "/api/v1/customers/",
            json={"name": f"C{i}", "email": f"c{i}@example.com"},
        )
    res = client.get("/api/v1/customers/")
    assert res.status_code == 200
    assert res.json()["total"] == 2


def test_update_customer(client: TestClient) -> None:
    c = client.post(
        "/api/v1/customers/",
        json={"name": "Old", "email": "old@example.com"},
    ).json()
    res = client.put(f"/api/v1/customers/{c['id']}", json={"name": "New"})
    assert res.status_code == 200
    assert res.json()["name"] == "New"


def test_delete_customer_without_orders(client: TestClient) -> None:
    c = client.post(
        "/api/v1/customers/",
        json={"name": "Delete Me", "email": "del@example.com"},
    ).json()
    res = client.delete(f"/api/v1/customers/{c['id']}")
    assert res.status_code == 204


def test_delete_customer_with_orders_blocked(client: TestClient) -> None:
    c = client.post(
        "/api/v1/customers/",
        json={"name": "Has Orders", "email": "ho@example.com"},
    ).json()
    p = client.post(
        "/api/v1/products/",
        json={"name": "Item", "sku": "I-1", "price": 1.0, "stock_quantity": 5},
    ).json()
    client.post(
        "/api/v1/orders/",
        json={
            "customer_id": c["id"],
            "items": [{"product_id": p["id"], "quantity": 1}],
        },
    )
    res = client.delete(f"/api/v1/customers/{c['id']}")
    assert res.status_code == 400
