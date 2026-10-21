# Cola nocturna: genera hasta $MaxEpisodes episodios pendientes con Wan2GP y los ensambla.
# Ejecutar en el PC NVIDIA. Requiere ffmpeg en PATH y Wan2GP instalado.
param(
    [string]$Wan2GPDir = 'C:\AI\Wan2GP',
    [string]$PythonExe = '',
    [int]$MaxEpisodes = 5,
    [int]$StopHour = 7          # no iniciar episodios nuevos a partir de esta hora de la manana
)
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
if (-not $PythonExe) { $PythonExe = Join-Path $Wan2GPDir 'venv\Scripts\python.exe' }
$logDir = Join-Path $root 'logs'; $outRoot = Join-Path $root 'output'; $done = Join-Path $root 'queue\done.txt'
New-Item -ItemType Directory -Force $logDir, $outRoot | Out-Null
if (-not (Test-Path $done)) { New-Item -ItemType File $done | Out-Null }
$log = Join-Path $logDir ((Get-Date -Format 'yyyy-MM-dd') + '.log')
function Log($m) { "$(Get-Date -Format 'HH:mm:ss') $m" | Tee-Object -FilePath $log -Append }

$lock = Join-Path $root 'queue\run.lock'
if (Test-Path $lock) { Log 'Otra ejecucion en curso (run.lock). Salgo.'; exit 1 }
New-Item -ItemType File $lock | Out-Null
try {
    $doneIds = @(Get-Content $done)
    $pending = Get-ChildItem (Join-Path $root 'episodes') -Directory | Where-Object { $doneIds -notcontains $_.Name } | Select-Object -First $MaxEpisodes
    $ok = @(); $fail = @()
    foreach ($ep in $pending) {
        $h = (Get-Date).Hour
        if ($h -ge $StopHour -and $h -lt 20) { Log "Pasadas las $StopHour:00, no inicio $($ep.Name)."; break }
        $out = Join-Path $outRoot $ep.Name
        $queue = Join-Path $ep.FullName 'queue.json'
        $success = $false
        foreach ($try in 1..2) {
            Remove-Item $out -Recurse -Force -ErrorAction SilentlyContinue
            New-Item -ItemType Directory -Force $out | Out-Null
            Log "$($ep.Name): intento $try"
            Push-Location $Wan2GPDir
            & $PythonExe wgp.py --process $queue --output-dir $out *>> $log
            Pop-Location
            $n = @(Get-ChildItem $out -Filter *.mp4 -ErrorAction SilentlyContinue).Count
            if ($n -ge 5) { $success = $true; break }
            Log "$($ep.Name): solo $n/5 clips"
        }
        if ($success) {
            try { & (Join-Path $PSScriptRoot 'assemble.ps1') -EpisodeDir $out -Name $ep.Name; Add-Content $done $ep.Name; $ok += $ep.Name; Log "$($ep.Name): LISTO" }
            catch { $fail += $ep.Name; Log "$($ep.Name): ensamble fallo: $_" }
        } else { $fail += $ep.Name }
    }
    $r = "Corrida $(Get-Date -Format 'yyyy-MM-dd HH:mm')`nTerminados: $($ok -join ', ')`nFallidos: $($fail -join ', ')`nPendientes: $((@(Get-ChildItem (Join-Path $root 'episodes') -Directory).Count) - @(Get-Content $done).Count)`nVideos: $outRoot\<epNN>\<epNN>_final.mp4`nRecordatorio: marcar contenido sintetico y 'para ninos' al subir; no publicar sin revisar."
    [IO.File]::WriteAllText((Join-Path $root 'LEEME_MANANA.txt'), $r)
    Log $r
} finally { Remove-Item $lock -Force -ErrorAction SilentlyContinue }
