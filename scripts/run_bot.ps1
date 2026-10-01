#Requires -Version 5.1
param(
    [string]$Log = "logs\job-bot_$(Get-Date -Format 'yyyyMMdd_HHmmss').log"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$logDir = Split-Path -Parent $Log
if ($logDir -and -not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir | Out-Null }

Write-Host "🤖 Ejecutando job-bot desde $root..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m src.main 2>&1 | ForEach-Object { "$_" } | Tee-Object -FilePath $Log

Write-Host "`n📄 Log guardado en: $root\$Log" -ForegroundColor Green