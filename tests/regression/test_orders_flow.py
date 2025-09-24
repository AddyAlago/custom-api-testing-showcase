import pytest
from src.utils.http import HttpClient

@pytest.mark.regression
def test_order_happy_path(base_url, session):
    client = HttpClient(base_url, session)

    # Precondition: create user
    u = client.post("/users", json={"name": "Grace", "email": "grace@example.com"})
    assert u.status_code == 201, f"User create failed: {u.status_code} {u.text} (Did you set API_TOKEN?)"
    user = u.json()
    assert "id" in user, f"No 'id' in user response: {user}"
    user_id = user["id"]

    # Create order
    o = client.post("/orders", json={"user_id": user_id, "items": [{"sku": "ABC", "qty": 2}]})
    assert o.status_code == 201, f"Order create failed: {o.status_code} {o.text}"
    order = o.json()
    assert "id" in order, f"No 'id' in order response: {order}"
    order_id = order["id"]

    # Get order
    g = client.get(f"/orders/{order_id}")
    assert g.status_code == 200, f"Get order failed: {g.status_code} {g.text}"
    body = g.json()
    assert isinstance(body.get("total"), (int, float)) and body["total"] > 0, f"Unexpected total: {body}"
