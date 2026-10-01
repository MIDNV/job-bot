#Requires -Version 5.1
$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

Write-Host "🔧 Creando entorno virtual en $root..." -ForegroundColor Cyan
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

Write-Host "📦 Instalando dependencias..." -ForegroundColor Cyan
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
    Write-Host "📝 Creado .env — edítalo con tus credenciales." -ForegroundColor Yellow
}

Write-Host "✅ Setup completo. Ejecuta: .\scripts\run_bot.ps1" -ForegroundColor Green