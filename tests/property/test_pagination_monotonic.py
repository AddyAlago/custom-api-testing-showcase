from hypothesis import given, strategies as st

@given(page=st.integers(min_value=1, max_value=5))
def test_users_pagination_monotonic(api_client, page):
    r1 = api_client.get("/users", params={"page": page, "size": 5})
    r2 = api_client.get("/users", params={"page": page + 1, "size": 5})
    assert r1.status_code == 200 and r2.status_code == 200
    a, b = r1.json(), r2.json()

    # Property: items are lists; and moving forward should not return *more*
    # earlier ids than previous page (very loose monotonicity check)
    assert isinstance(a, list) and isinstance(b, list)
    if a and b and isinstance(a[0], dict) and isinstance(b[0], dict) and "id" in a[0] and "id" in b[0]:
        assert min(x["id"] for x in b) >= min(x["id"] for x in a)
