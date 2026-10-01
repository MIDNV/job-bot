#Requires -Version 5.1

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$Log = "logs\job-bot_$timestamp.log"

$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"

$logDir = Split-Path -Parent $Log
if ($logDir -and -not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

Write-Host "Ejecutando job-bot desde $root..." -ForegroundColor Cyan
Write-Host ""

$prevErrorAction = $ErrorActionPreference
$ErrorActionPreference = "Continue"

& ".\.venv\Scripts\python.exe" -m src.main *>&1 | Tee-Object -FilePath $Log

$ErrorActionPreference = $prevErrorAction

Write-Host ""
Write-Host "Log guardado en: $root\$Log" -ForegroundColor Green