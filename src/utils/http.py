from typing import Any, Dict, Optional
import requests


class HttpClient:
    def __init__(self, base_url: str, session: requests.Session):
        self.base_url = base_url.rstrip('/')
        self.session = session


    def get(self, path: str, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)


    def post(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs):
        return self.session.post(f"{self.base_url}{path}", json=json, **kwargs)


    def put(self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs):
        return self.session.put(f"{self.base_url}{path}", json=json, **kwargs)


    def delete(self, path: str, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", **kwargs)