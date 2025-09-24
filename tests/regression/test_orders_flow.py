import pytest
from src.utils.http import HttpClient

@pytest.mark.regression
def test_order_happy_path(base_url, session):
    client = HttpClient(base_url, session)

    # Precondition: create user
    u = client.post("/users", json={"name": "Grace", "email": "grace@example.com"})
    user_id = u.json()["id"]

    # Create order
    o = client.post("/orders", json={"user_id": user_id, "items": [{"sku": "ABC", "qty": 2}]})
    assert o.status_code == 201
    order_id = o.json()["id"]

    # Get order
    g = client.get(f"/orders/{order_id}")
    assert g.status_code == 200
    assert g.json()["total"] > 0
