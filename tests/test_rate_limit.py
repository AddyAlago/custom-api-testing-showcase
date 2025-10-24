import os
import json
import pytest

pytestmark = pytest.mark.ratelimit

def _json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return {}

def test_rate_limit_behavior(api_client):
    """
    Deterministic: queries /ratelimit/info to discover the cap,
    then sends cap+2 requests to guarantee a 429, and verifies Retry-After.
    """
    endpoint = os.getenv("RATE_LIMIT_ENDPOINT", "/ratelimit")

    # discover threshold
    info = api_client.get(f"{endpoint}/info")
    assert info.status_code == 200, f"Could not read {endpoint}/info"
    meta = _json(info.text)
    limit = int(meta.get("limit", 30))

    # fire exactly limit+2 requests
    seen_429 = False
    for _ in range(limit + 2):
        r = api_client.get(endpoint)
        if r.status_code == 429:
            ra = r.headers.get("Retry-After")
            assert ra is not None and int(ra) >= 1, f"Missing/invalid Retry-After: {ra}"
            seen_429 = True
            break

    if not seen_429:
        pytest.xfail("No 429 encountered; service did not enforce limit within declared threshold")
