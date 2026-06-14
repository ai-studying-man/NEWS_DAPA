$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $RepoRoot

if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

$uv = Get-Command uv -ErrorAction SilentlyContinue
if ($null -ne $uv) {
    & uv run dapa-morning-brief --days 3 --fallback-days 5 *>> "logs\dapa_morning_brief.log"
    exit $LASTEXITCODE
}

$env:PYTHONPATH = Join-Path $RepoRoot "src"
& python -m dapa_morning_brief.cli --days 3 --fallback-days 5 *>> "logs\dapa_morning_brief.log"
exit $LASTEXITCODE
