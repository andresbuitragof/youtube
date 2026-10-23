# Une los clips de un episodio (orden por fecha de creacion) en <ep>_mudo.mp4 con ffmpeg y,
# si hay voz, mezcla narracion (+ musica opcional) en <ep>_final.mp4. Sin voz, final = mudo.
param(
    [Parameter(Mandatory)][string]$EpisodeDir,
    [Parameter(Mandatory)][string]$Name,
    [string]$Voice = '',
    [string]$Music = ''
)
$ErrorActionPreference = 'Stop'
$clips = Get-ChildItem $EpisodeDir -Filter *.mp4 | Where-Object { $_.Name -match '_seed\d+_' } | Sort-Object CreationTime
$list = Join-Path $EpisodeDir 'concat.txt'
$lines = $clips | ForEach-Object { "file '" + $_.FullName.Replace('\', '/').Replace("'", "'\''") + "'" }
[IO.File]::WriteAllLines($list, $lines, (New-Object System.Text.UTF8Encoding($false)))
$mudo = Join-Path $EpisodeDir "$Name`_mudo.mp4"
$final = Join-Path $EpisodeDir "$Name`_final.mp4"
& ffmpeg -y -loglevel error -f concat -safe 0 -i $list -c:v libx264 -pix_fmt yuv420p -crf 18 $mudo
if ($LASTEXITCODE -ne 0) { throw "ffmpeg fallo para $Name" }

if ($Voice -and (Test-Path $Voice)) {
    $vd = [double](& ffprobe -v error -show_entries format=duration -of csv=p=0 $mudo)
    $ad = [double](& ffprobe -v error -show_entries format=duration -of csv=p=0 $Voice)
    # acelera la voz solo si no cabe (maximo 1.25x); si aun asi no cabe, alarga el video
    # repitiendo el ultimo cuadro para no cortar la moraleja
    $tempo = [math]::Round([math]::Min(1.25, [math]::Max(1.0, $ad / ($vd - 0.8))), 3)
    $total = [math]::Round([math]::Max($vd, $ad / $tempo + 0.7), 2)
    $pad = [math]::Round($total - $vd, 2)
    $fadeAt = [math]::Round($total - 1.3, 2)
    $ff = @('-y', '-loglevel', 'error', '-i', $mudo, '-i', $Voice)
    if ($pad -gt 0) { $vf = "[0:v]tpad=stop_mode=clone:stop_duration=$pad[vv];"; $vmap = '[vv]'; $vcodec = @('-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18') }
    else { $vf = ''; $vmap = '0:v'; $vcodec = @('-c:v', 'copy') }
    if ($Music -and (Test-Path $Music)) {
        $ff += @('-i', $Music)
        $mFade = [math]::Round($total - 1.8, 2)
        $fc = "$vf[1:a]atempo=$tempo[v];[2:a]volume=0.22,afade=t=out:st=$($mFade):d=1.8[m];[v][m]amix=inputs=2:duration=longest:normalize=0,atrim=0:$total,afade=t=out:st=$($fadeAt):d=1.3[a]"
    } else {
        $fc = "$vf[1:a]atempo=$tempo,atrim=0:$total,afade=t=out:st=$($fadeAt):d=1.3[a]"
    }
    $ff += @('-filter_complex', $fc, '-map', $vmap, '-map', '[a]') + $vcodec + @('-c:a', 'aac', '-b:a', '160k', '-t', "$total", $final)
    & ffmpeg @ff
    if ($LASTEXITCODE -ne 0) { throw "mezcla de audio fallo para $Name" }
} else {
    Copy-Item $mudo $final -Force
}