# tests/utils/http_client.py
import time
from typing import Optional, Dict

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

try:
    import allure  # type: ignore
except Exception:
    allure = None


class APIClient:
    def __init__(
        self,
        base_url: str,
        token: Optional[str] = None,
        timeout: float = 30.0,
        retries: int = 3,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        retry_strategy = Retry(
            total=retries,
            connect=retries,
            read=retries,
            backoff_factor=0.5,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]),
            raise_on_status=False,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=10, pool_maxsize=20)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.default_headers: Dict[str, str] = {"Accept": "application/json"}
        if token:
            if token.lower().startswith("bearer "):
                self.default_headers["Authorization"] = token
            else:
                self.default_headers["Authorization"] = f"Bearer {token}"

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = kwargs.pop("headers", {})
        merged_headers = {**self.default_headers, **headers}

        start = time.perf_counter()
        resp = self.session.request(method.upper(), url, headers=merged_headers, timeout=self.timeout, **kwargs)
        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        if allure:
            with allure.step(f"{method.upper()} {url} [{resp.status_code}] in {elapsed_ms}ms"):
                allure.attach(
                    str(merged_headers),
                    name="request_headers",
                    attachment_type=allure.attachment_type.TEXT,
                )
                if kwargs.get("json") is not None:
                    allure.attach(
                        json_dumps(kwargs["json"]),
                        name="request_json",
                        attachment_type=allure.attachment_type.JSON,
                    )
                allure.attach(
                    resp.text,
                    name="response_body",
                    attachment_type=(
                        allure.attachment_type.JSON
                        if "application/json" in resp.headers.get("Content-Type", "")
                        else allure.attachment_type.TEXT
                    ),
                )

        return resp

    # Convenience wrappers (must be indented inside the class)
    def get(self, path: str, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path: str, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path: str, **kwargs):
        return self.request("PUT", path, **kwargs)

    def patch(self, path: str, **kwargs):
        return self.request("PATCH", path, **kwargs)

    def delete(self, path: str, **kwargs):
        return self.request("DELETE", path, **kwargs)


def json_dumps(obj) -> str:
    try:
        import json
        return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)
    except Exception:
        return str(obj)
