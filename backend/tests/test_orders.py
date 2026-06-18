"""Order API tests, including stock validation and inventory deduction."""
from fastapi.testclient import TestClient


def _make_customer(client: TestClient) -> int:
    res = client.post(
        "/api/v1/customers/",
        json={"name": "Buyer", "email": "buyer@example.com"},
    )
    assert res.status_code == 201
    return res.json()["id"]


def _make_product(client: TestClient, sku: str, price: float, stock: int) -> int:
    res = client.post(
        "/api/v1/products/",
        json={"name": sku, "sku": sku, "price": price, "stock_quantity": stock},
    )
    assert res.status_code == 201
    return res.json()["id"]


def test_create_order_success(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "O-1", 10.0, 5)
    res = client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 2}]},
    )
    assert res.status_code == 201
    data = res.json()
    assert data["customer_id"] == customer
    assert float(data["total_amount"]) == 20.0
    assert len(data["items"]) == 1
    assert data["items"][0]["subtotal"] == "20.00"

    # Stock should be decremented
    p = client.get(f"/api/v1/products/{product}").json()
    assert p["stock_quantity"] == 3


def test_create_order_multiple_items(client: TestClient) -> None:
    customer = _make_customer(client)
    p1 = _make_product(client, "M-1", 10.0, 5)
    p2 = _make_product(client, "M-2", 5.0, 10)
    res = client.post(
        "/api/v1/orders/",
        json={
            "customer_id": customer,
            "items": [
                {"product_id": p1, "quantity": 2},
                {"product_id": p2, "quantity": 4},
            ],
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert float(data["total_amount"]) == 40.0  # 2*10 + 4*5


def test_create_order_insufficient_stock_returns_400(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "S-1", 10.0, 1)
    res = client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 5}]},
    )
    assert res.status_code == 400
    assert "Insufficient stock" in res.json()["detail"]
    # Stock unchanged
    p = client.get(f"/api/v1/products/{product}").json()
    assert p["stock_quantity"] == 1


def test_create_order_unknown_customer_returns_404(client: TestClient) -> None:
    product = _make_product(client, "U-1", 1.0, 5)
    res = client.post(
        "/api/v1/orders/",
        json={"customer_id": 9999, "items": [{"product_id": product, "quantity": 1}]},
    )
    assert res.status_code == 404


def test_create_order_unknown_product_returns_404(client: TestClient) -> None:
    customer = _make_customer(client)
    res = client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": 9999, "quantity": 1}]},
    )
    assert res.status_code == 404


def test_create_order_zero_quantity_rejected(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "Z-1", 1.0, 5)
    res = client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 0}]},
    )
    assert res.status_code == 422


def test_create_order_empty_items_rejected(client: TestClient) -> None:
    customer = _make_customer(client)
    res = client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": []},
    )
    assert res.status_code == 422


def test_list_orders(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "L-1", 1.0, 5)
    client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 1}]},
    )
    res = client.get("/api/v1/orders/")
    assert res.status_code == 200
    assert res.json()["total"] == 1


def test_get_order_by_id(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "G-1", 1.0, 5)
    created = client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 1}]},
    ).json()
    res = client.get(f"/api/v1/orders/{created['id']}")
    assert res.status_code == 200
    assert res.json()["id"] == created["id"]


def test_dashboard_stats(client: TestClient) -> None:
    customer = _make_customer(client)
    product = _make_product(client, "D-1", 1.0, 1)
    client.post(
        "/api/v1/orders/",
        json={"customer_id": customer, "items": [{"product_id": product, "quantity": 1}]},
    )
    res = client.get("/api/v1/dashboard/")
    assert res.status_code == 200
    data = res.json()
    assert data["total_products"] == 1
    assert data["total_customers"] == 1
    assert data["total_orders"] == 1
    assert any(p["id"] == product for p in data["low_stock_products"])


def test_cancel_order_restores_stock(client: TestClient) -> None:
    """When an order is cancelled, stock should be restored."""
    customer = _make_customer(client)
    product = _make_product(client, "C-1", 10.0, 10)

    # Place an order that takes 4 units
    created = client.post(
        "/api/v1/orders/",
        json={
            "customer_id": customer,
            "items": [{"product_id": product, "quantity": 4}],
        },
    ).json()

    # Stock should now be 6
    p = client.get(f"/api/v1/products/{product}").json()
    assert p["stock_quantity"] == 6

    # Cancel the order
    res = client.delete(f"/api/v1/orders/{created['id']}")
    assert res.status_code == 204

    # Stock should be back to 10
    p = client.get(f"/api/v1/products/{product}").json()
    assert p["stock_quantity"] == 10

    # Order should be gone
    assert client.get(f"/api/v1/orders/{created['id']}").status_code == 404


def test_cancel_order_not_found(client: TestClient) -> None:
    res = client.delete("/api/v1/orders/9999")
    assert res.status_code == 404
