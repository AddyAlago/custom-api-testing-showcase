from src.utils.http import HttpClient

def test_unauthorized_without_token(base_url, session, monkeypatch):
    # Remove token for this request
    s = session
    s.headers.pop("Authorization", None)
    client = HttpClient(base_url, s)
    r = client.get("/orders")
    assert r.status_code in (401, 403)

def test_validation_error(base_url, session):
    client = HttpClient(base_url, session)
    r = client.post("/users", json={"name": "", "email": "not-an-email"})
    assert r.status_code == 400
