<#
.SYNOPSIS
    Programa el bot para que se ejecute automáticamente cada día a las 9:00.
.DESCRIPTION
    Crea una tarea en el Programador de Tareas de Windows llamada "JobBot"
    que ejecuta run_bot.ps1 todos los días a la hora indicada.
.NOTES
    Ejecuta este script UNA SOLA VEZ. Si lo vuelves a ejecutar, sobreescribe
    la tarea existente (no crea duplicados).
#>

# ----- Configuración -----
$TaskName = "JobBot"
$HoraEjecucion = "9am"      # puedes cambiarlo: "8am", "10:30am", "6pm", etc.
$Descripcion = "Busca ofertas de empleo relacionadas con el CV de Glen Owen Diaz Thornton"

# ----- Calcular la ruta absoluta de run_bot.ps1 -----
$root = Split-Path -Parent $PSScriptRoot
$runScript = Join-Path $root "scripts\run_bot.ps1"

# ----- Comprobaciones previas -----
if (-not (Test-Path $runScript)) {
    Write-Host "❌ No se encontró $runScript" -ForegroundColor Red
    Write-Host "   Asegúrate de haber creado run_bot.ps1 en la carpeta scripts\" -ForegroundColor Yellow
    exit 1
}

Write-Host "📅 Programando tarea '$TaskName' para las $HoraEjecucion..." -ForegroundColor Cyan
Write-Host "   Script a ejecutar: $runScript" -ForegroundColor Gray

# ----- Definir qué se ejecuta -----
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$runScript`""

# ----- Definir cuándo se ejecuta -----
$trigger = New-ScheduledTaskTrigger -Daily -At $HoraEjecucion

# ----- Definir con qué usuario -----
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

# ----- Registrar la tarea (sobrescribe si ya existe) -----
Register-ScheduledTask -TaskName $TaskName `
    -Action $action `
    -Trigger $trigger `
    -Principal $principal `
    -Description $Descripcion `
    -Force | Out-Null

Write-Host "✅ Tarea '$TaskName' programada correctamente." -ForegroundColor Green
Write-Host ""
Write-Host "Comandos útiles:" -ForegroundColor Cyan
Write-Host "  Ver la tarea:        Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "  Ejecutarla ahora:    Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "  Ver último estado:   Get-ScheduledTaskInfo -TaskName '$TaskName'" -ForegroundColor Gray
Write-Host "  Eliminarla:          Unregister-ScheduledTask -TaskName '$TaskName' -Confirm:`$false" -ForegroundColor Gray