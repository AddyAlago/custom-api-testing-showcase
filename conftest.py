import os
import pytest
import requests
from dotenv import load_dotenv

# --- Load env ---
load_dotenv()

@pytest.fixture(scope="session")
def base_url() -> str:
    return os.getenv("BASE_URL", "http://localhost:8000")

@pytest.fixture(scope="session")
def session() -> requests.Session:
    s = requests.Session()
    token = os.getenv("API_TOKEN")
    if token:
        s.headers.update({"Authorization": f"Bearer {token}"})
    s.headers.update({"Content-Type": "application/json"})
    return s

# --- Allure labeling so this suite merges nicely with your portfolio report ---
try:
    import allure  # type: ignore
except Exception:  # pragma: no cover
    allure = None


def _infer_subsuite(nodeid: str) -> str:
    # nodeid like: tests/regression/test_users_crud.py::TestUsersCrud::test_...
    if "tests/regression/" in nodeid:
        return "Regression"
    if "tests/contract/" in nodeid:
        return "Contract"
    if "tests/negative/" in nodeid:
        return "Negative"
    if "tests/smoke/" in nodeid:
        return "Smoke"
    return "API"


def pytest_collection_modifyitems(items):
    if not allure:
        return
    for item in items:
        # Top-level group in your existing portfolio report
        item.add_marker(allure.label("parentSuite", "Portfolio"))
        # This project label helps when merging cross-repo
        item.add_marker(allure.label("epic", "API Testing Showcase"))
        # Show a dedicated suite for API
        item.add_marker(allure.label("suite", "API"))
        # Group by folder as subSuite
        item.add_marker(allure.label("subSuite", _infer_subsuite(item.nodeid)))
