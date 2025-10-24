$ErrorActionPreference = "Stop"
Push-Location "$PSScriptRoot/../local-api"
docker compose -f docker-compose.api.yml down
Pop-Location
