param(
  [int]$ApiPort = 8000,
  [int]$WebPort = 3000,
  [string]$Python = ".\.venv\Scripts\python.exe",
  [string]$Pnpm = "pnpm"
)

$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$env:PYTHONPATH = $root
$env:NEXT_PUBLIC_API_BASE_URL = "http://127.0.0.1:$ApiPort"

if (!(Test-Path $Python)) {
  Write-Host "Python environment not found. Run scripts\verify.ps1 first."
  exit 1
}

Write-Host "Starting VolEdge API on http://127.0.0.1:$ApiPort"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:PYTHONPATH='$root'; & '$Python' -m uvicorn apps.api.app.main:app --host 127.0.0.1 --port $ApiPort"

Write-Host "Starting VolEdge web app on http://127.0.0.1:$WebPort"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:NEXT_PUBLIC_API_BASE_URL='http://127.0.0.1:$ApiPort'; & '$Pnpm' --dir apps/web dev --hostname 127.0.0.1 --port $WebPort"

Write-Host "Open http://127.0.0.1:$WebPort after both windows say ready."
