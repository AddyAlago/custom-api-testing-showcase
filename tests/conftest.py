import os
import json
import pytest
from pathlib import Path
from tests.utils.http_client import APIClient

def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=None, help="Base URL for the API under test")
    parser.addoption("--api-token", action="store", default=None, help="Bearer token or API key")

@pytest.fixture(scope="session")
def base_url(pytestconfig):
    # Priority: CLI flag > ENV var > skip
    url = pytestconfig.getoption("--base-url") or os.getenv("API_BASE_URL")
    if not url:
        pytest.skip("No base URL provided. Use --base-url or set API_BASE_URL.")
    return url.rstrip("/")

@pytest.fixture(scope="session")
def api_token(pytestconfig):
    return pytestconfig.getoption("--api-token") or os.getenv("API_TOKEN")

@pytest.fixture(scope="session")
def api_client(base_url, api_token):
    return APIClient(base_url=base_url, token=api_token)

@pytest.fixture(scope="session")
def load_schema():
    def _load(name: str):
        here = Path(__file__).resolve().parent
        schema_path = here / "schemas" / f"{name}.json"
        if not schema_path.exists():
            pytest.skip(f"Schema file not found: {schema_path}")
        return json.loads(schema_path.read_text(encoding="utf-8"))
    return _load
