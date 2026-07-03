param(
  [Parameter(Mandatory = $true)]
  [string]$RemoteUrl
)

$ErrorActionPreference = "Stop"

if (!(Test-Path ".git")) {
  git init -b main
}

$status = git status --short
if ($status) {
  git add -A
  git commit -m "Prepare VolEdge AI production app"
}

$existing = git remote
if ($existing -contains "origin") {
  git remote set-url origin $RemoteUrl
} else {
  git remote add origin $RemoteUrl
}

git push -u origin main
Write-Host "Pushed VolEdge AI to $RemoteUrl"
