Param(
    [string]$BaseUrl = "http://localhost:8000",
    [string]$Token = ""
)

$ErrorActionPreference = "Stop"

# Point tests at local API
$env:API_BASE_URL = $BaseUrl

# Only set API_TOKEN if provided (useful when REQUIRE_AUTH=1 in the API)
if ($Token -ne "") {
    $env:API_TOKEN = $Token
}

# Optional endpoints (uncomment to customize)
# $env:IDEMPOTENT_CREATE_PATH = "/orders"
# $env:RATE_LIMIT_ENDPOINT    = "/ratelimit"

# Run a useful default selection of suites
pytest -m "contract or negative or idempotency" -q
