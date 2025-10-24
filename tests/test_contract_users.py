import pytest
import jsonschema

pytestmark = pytest.mark.contract

@pytest.mark.parametrize("path,schema_name", [
    ("/users", "user_list"),
])
def test_list_contract(api_client, load_schema, path, schema_name):
    schema = load_schema(schema_name)
    res = api_client.get(path)
    assert res.status_code == 200, f"Unexpected status: {res.status_code} body={res.text[:500]}"
    data = res.json()
    jsonschema.validate(instance=data, schema=schema)

@pytest.mark.parametrize("user_id", [1])
def test_get_by_id_contract(api_client, load_schema, user_id):
    schema = load_schema("user")
    res = api_client.get(f"/users/{user_id}")
    assert res.status_code in (200, 404), f"Unexpected status: {res.status_code} body={res.text[:500]}"
    if res.status_code == 200:
        jsonschema.validate(instance=res.json(), schema=schema)
    else:
        pytest.skip("User not found in target environment")
