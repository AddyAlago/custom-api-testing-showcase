# Robust Local API (FastAPI)
Run a local API with endpoints your tests expect.

## Run with Docker
```powershell
docker compose up --build
```
API: http://localhost:8000  | Docs: http://localhost:8000/docs

## Run with Python (no Docker)
```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Env toggles
- REQUIRE_AUTH=1 — require Authorization: Bearer <token>
- RATE_LIMIT_PER_MIN=30 — limit for /ratelimit

## Point tests
```powershell
$env:API_BASE_URL = "http://localhost:8000"
pytest -m "contract or negative or idempotency" -q
```
