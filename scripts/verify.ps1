param(
  [string]$Python = ".\.venv\Scripts\python.exe",
  [string]$Pnpm = "pnpm"
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $Python)) {
  Write-Host "Creating local Python environment..."
  python -m venv .venv
  $Python = ".\.venv\Scripts\python.exe"
}

Write-Host "Installing API dependencies..."
& $Python -m pip install -r apps/api/requirements.txt

Write-Host "Running backend tests..."
$env:PYTHONPATH = (Get-Location).Path
& $Python -m pytest

Write-Host "Installing web dependencies..."
& $Pnpm --dir apps/web install --no-frozen-lockfile

Write-Host "Building web app..."
& $Pnpm --dir apps/web build

Write-Host "Verification complete."
