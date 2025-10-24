Param(
    [switch]$Rebuild  # use -Rebuild to force image rebuild
)

$ErrorActionPreference = "Stop"

# Go to local-api directory
Push-Location "$PSScriptRoot/../local-api"

# Compose file name (we use a custom name to avoid conflicts)
$composeFile = "docker-compose.api.yml"

# Build args
if ($Rebuild) {
    docker compose -f $composeFile up --build
} else {
    docker compose -f $composeFile up
}

Pop-Location
