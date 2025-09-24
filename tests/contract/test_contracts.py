import json
from pathlib import Path
import pytest
from jsonschema import validate
from src.utils.http import HttpClient

SCHEMAS = {
    "user": json.loads((Path(__file__).parent / "schemas" / "user.schema.json").read_text()),
    "order": json.loads((Path(__file__).parent / "schemas" / "order.schema.json").read_text()),
}

@pytest.mark.contract
def test_user_contract(base_url, session):
    client = HttpClient(base_url, session)
    created = client.post("/users", json={"name": "Lin", "email": "lin@example.com"})
    assert created.status_code == 201
    validate(instance=created.json(), schema=SCHEMAS["user"])

@pytest.mark.contract
def test_order_contract(base_url, session):
    client = HttpClient(base_url, session)
    u = client.post("/users", json={"name": "Max", "email": "max@example.com"}).json()
    created = client.post("/orders", json={"user_id": u["id"], "items": [{"sku": "XYZ", "qty": 1}]})
    assert created.status_code == 201
    validate(instance=created.json(), schema=SCHEMAS["order"])
