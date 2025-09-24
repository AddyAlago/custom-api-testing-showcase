import requests
from src.utils.http import HttpClient


def test_unauthorized_without_token(base_url, session, monkeypatch):
    # Use a fresh session with NO auth so we don't mutate the shared fixture
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    client = HttpClient(base_url, s)
    r = client.get("/orders")
    assert r.status_code in (401, 403)


def test_validation_error(base_url, session):
    client = HttpClient(base_url, session)
    r = client.post("/users", json={"name": "", "email": "not-an-email"})
    # FastAPI/Pydantic raises 422 for body validation errors
    assert r.status_code == 422
