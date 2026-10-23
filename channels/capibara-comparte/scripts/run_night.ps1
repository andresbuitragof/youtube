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
function Log($m) { "$(Get-Date -Format 'HH:mm:ss') $m" | Tee-Object -FilePath $log -Append | Out-Host }

# Genera un audio con wgp.py (voz o musica) y devuelve la ruta del .wav, o '' si falla.
function New-Audio($settings, $outDir, $label) {
    foreach ($try in 1..2) {
        Remove-Item $outDir -Recurse -Force -ErrorAction SilentlyContinue
        New-Item -ItemType Directory -Force $outDir | Out-Null
        Log "${label}: intento $try"
        Push-Location $Wan2GPDir
        & $PythonExe wgp.py --process $settings --output-dir $outDir *>> $log
        Pop-Location
        $wav = Get-ChildItem $outDir -Filter *.wav -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($wav) { return $wav.FullName }
    }
    Log "${label}: no se genero audio"
    return ''
}
# Musica de tema: se genera una vez y se reutiliza en todos los episodios.
$assets = Join-Path $root 'assets'; New-Item -ItemType Directory -Force $assets | Out-Null
$musicFile = Join-Path $assets 'musica_tema.wav'

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
            if (-not (Test-Path $musicFile)) {
                $m = New-Audio (Join-Path $root 'queue\musica.json') (Join-Path $outRoot '_musica') 'musica'
                if ($m) { Copy-Item $m $musicFile -Force }
            }
            $voz = New-Audio (Join-Path $ep.FullName 'voz.json') (Join-Path $out 'audio') "$($ep.Name) voz"
            if (-not $voz) { Log "$($ep.Name): sin voz, se ensambla mudo" }
            try { & (Join-Path $PSScriptRoot 'assemble.ps1') -EpisodeDir $out -Name $ep.Name -Voice $voz -Music $musicFile; Add-Content $done $ep.Name; $ok += $ep.Name; Log "$($ep.Name): LISTO" }
            catch { $fail += $ep.Name; Log "$($ep.Name): ensamble fallo: $_" }
        } else { $fail += $ep.Name }
    }
    $r = "Corrida $(Get-Date -Format 'yyyy-MM-dd HH:mm')`nTerminados: $($ok -join ', ')`nFallidos: $($fail -join ', ')`nPendientes: $((@(Get-ChildItem (Join-Path $root 'episodes') -Directory).Count) - @(Get-Content $done).Count)`nVideos: $outRoot\<epNN>\<epNN>_final.mp4`nRecordatorio: marcar contenido sintetico y 'para ninos' al subir; no publicar sin revisar."
    [IO.File]::WriteAllText((Join-Path $root 'LEEME_MANANA.txt'), $r)
    Log $r
} finally { Remove-Item $lock -Force -ErrorAction SilentlyContinue }
