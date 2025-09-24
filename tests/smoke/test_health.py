import pytest
from src.utils.http import HttpClient

@pytest.mark.smoke
def test_health_ok(base_url, session):
    client = HttpClient(base_url, session)
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"
