# Registra la tarea diaria (23:00) en el PC NVIDIA. Ejecutar como el usuario que usara Wan2GP.
param([string]$Wan2GPDir = 'C:\AI\Wan2GP', [string]$At = '23:00')
$script = Join-Path $PSScriptRoot 'run_night.ps1'
$action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$script`" -Wan2GPDir `"$Wan2GPDir`""
$trigger = New-ScheduledTaskTrigger -Daily -At $At
$settings = New-ScheduledTaskSettingsSet -WakeToRun -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Hours 9)
Register-ScheduledTask -TaskName 'CapibaraComparte-Noche' -Action $action -Trigger $trigger -Settings $settings -Force
Write-Host "Tarea registrada: diaria a las $At. Prueba: Start-ScheduledTask -TaskName CapibaraComparte-Noche"
