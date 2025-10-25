import re
from hypothesis import given, strategies as st

# Simple email strategy
EMAILS = st.emails()

@given(EMAILS)
def test_user_creation_normalizes_email(api_client, email):
    # Create a user with mixed-case/local+tags spacing
    payload = {"name": "Prop Test", "email": email}
    r = api_client.post("/users", json=payload)
    assert r.status_code in (200, 201, 202), r.text
    data = r.json()
    assert "email" in data

    # Property we expect: lowercase & trimmed email
    assert data["email"] == email.strip().lower()
    # Bonus: basic sanity
    assert "@" in data["email"]
