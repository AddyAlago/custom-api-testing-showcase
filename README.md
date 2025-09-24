# API Testing Showcase

Production-style API testing: functional, contract, performance, and security checks with CI and reports.

![CI](https://img.shields.io/github/actions/workflow/status/OWNER/REPO/api-tests.yml?label=CI)
![Allure](https://img.shields.io/badge/report-Allure-blue)

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
