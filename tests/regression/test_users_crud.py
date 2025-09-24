import pytest
from src.utils.http import HttpClient

@pytest.mark.regression
class TestUsersCrud:
    def test_create_read_update_delete_user(self, base_url, session):
        client = HttpClient(base_url, session)
        payload = {"name": "Ada", "email": "ada@example.com"}

        # Create
        created = client.post("/users", json=payload)
        assert created.status_code == 201
        user = created.json()
        user_id = user["id"]

        # Read
        got = client.get(f"/users/{user_id}")
        assert got.status_code == 200
        assert got.json()["email"] == payload["email"]

        # update
        upd = client.put(f"/users/{user_id}", json={"name": "Ada Lovelace", "email": payload["email"]})
        assert upd.status_code == 200
        assert upd.json()["name"] == "Ada Lovelace"


        # Delete
        deleted = client.delete(f"/users/{user_id}")
        assert deleted.status_code == 204

        # Verify gone
        missing = client.get(f"/users/{user_id}")
        assert missing.status_code == 404
