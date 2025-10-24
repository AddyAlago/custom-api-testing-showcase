import pytest

pytestmark = pytest.mark.negative

@pytest.mark.parametrize("payload,field", [
    ({"name": ""}, "name"),
    ({"email": "not-an-email"}, "email"),
])
def test_create_user_invalid_input(api_client, payload, field):
    res = api_client.post("/users", json=payload)
    assert res.status_code in (400, 422), f"Expected validation error, got {res.status_code}"
    body = res.json() if "application/json" in res.headers.get("Content-Type","") else {}
    msg = str(body)
    assert field in msg or "error" in body or "errors" in body, f"Error response did not mention '{field}': {body}"
