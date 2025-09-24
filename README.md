# API Testing Showcase

### 🧪 API Test Suites

[![Smoke](https://github.com/<USER>/<REPO>/actions/workflows/smoke.yml/badge.svg?branch=main)](https://github.com/<USER>/<REPO>/actions/workflows/smoke.yml)
[![Regression](https://github.com/<USER>/<REPO>/actions/workflows/regression.yml/badge.svg?branch=main)](https://github.com/<USER>/<REPO>/actions/workflows/regression.yml)
[![Contract](https://github.com/<USER>/<REPO>/actions/workflows/contract.yml/badge.svg?branch=main)](https://github.com/<USER>/<REPO>/actions/workflows/contract.yml)
[![Negative](https://github.com/<USER>/<REPO>/actions/workflows/negative.yml/badge.svg?branch=main)](https://github.com/<USER>/<REPO>/actions/workflows/negative.yml)


### 📈 Performance

[![Performance](https://github.com/<USER>/<REPO>/actions/workflows/performance.yml/badge.svg?branch=main)](https://github.com/<USER>/<REPO>/actions/workflows/performance.yml)

### 🔐 Security

[![Security](https://github.com/<USER>/<REPO>/actions/workflows/security.yml/badge.svg?branch=main)](https://github.com/<USER>/<REPO>/actions/workflows/security.yml)

## Quick start

```bash
# 1) Run the mock API and k6/ZAP dependencies
docker compose up -d

# 2) Create a .env file with base URL and token (if needed)
cp .env.example .env

# 3) Install and run tests
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest -m smoke --alluredir=allure-results/smoke
pytest -m regression --alluredir=allure-results/regression
pytest -m contract --alluredir=allure-results/contract

# 4) Serve the Allure report locally
allure serve allure-results
```

## Target under test
- Default is a local FastAPI app (`http://localhost:8000`) exposing `/health`, `/users`, and `/orders` endpoints.
- You can point tests at any environment by setting `BASE_URL`.

## Test types
- **Smoke**: fast health and key endpoint checks.
- **Regression**: CRUD, flows, auth.
- **Contract**: JSON Schema validation.
- **Negative**: invalid inputs, missing auth, rate limits.
- **Performance**: k6 smoke.
- **Security**: ZAP baseline.

## Repo highlights
- **Fixtures** for base URL, auth, and data factories
- **JSON Schemas** in `tests/contract/schemas`
- **Data-driven** tests via CSV in `tests/data`
- **CI** with matrix for suites and artifacts upload

## Badges
Add real badges after pushing:
```md
![CI](https://img.shields.io/github/actions/workflow/status/<owner>/<repo>/api-tests.yml?branch=main)
[Allure report](https://<owner>.github.io/<repo>/)
```
