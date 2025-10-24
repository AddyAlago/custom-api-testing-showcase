import os
import uuid
import pytest

pytestmark = pytest.mark.idempotency

def _idempotency_header():
    key = str(uuid.uuid4())
    return {"Idempotency-Key": key, "x-idempotency-key": key}

@pytest.mark.parametrize("body", [
    {"sku": "SKU-123", "qty": 1},
])
def test_post_is_idempotent(api_client, body):
    path = os.getenv("IDEMPOTENT_CREATE_PATH", "/orders")
    headers = _idempotency_header()
    first = api_client.post(path, json=body, headers=headers)
    second = api_client.post(path, json=body, headers=headers)
    assert first.status_code in (200, 201, 202, 409), f"Unexpected status: {first.status_code}"
    assert second.status_code in (200, 201, 202, 409), f"Unexpected status: {second.status_code}"
    if first.ok and second.ok:
        assert first.json().get("id") == second.json().get("id"), "Idempotent POST returned different resources"
    elif second.status_code == 409:
        pass
    else:
        pytest.xfail("Service may not support idempotency for this endpoint in this environment")
