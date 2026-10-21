# Une los clips de un episodio (orden por fecha de creacion) en <ep>_final.mp4 con ffmpeg.
param([Parameter(Mandatory)][string]$EpisodeDir, [Parameter(Mandatory)][string]$Name)
$ErrorActionPreference = 'Stop'
$clips = Get-ChildItem $EpisodeDir -Filter *.mp4 | Where-Object { $_.Name -notlike '*_final.mp4' } | Sort-Object CreationTime
$list = Join-Path $EpisodeDir 'concat.txt'
$lines = $clips | ForEach-Object { "file '" + ($_.FullName -replace '\', '/') + "'" }
[IO.File]::WriteAllLines($list, $lines, (New-Object System.Text.UTF8Encoding($false)))
& ffmpeg -y -loglevel error -f concat -safe 0 -i $list -c:v libx264 -pix_fmt yuv420p -crf 18 (Join-Path $EpisodeDir "$Name`_final.mp4")
if ($LASTEXITCODE -ne 0) { throw "ffmpeg fallo para $Name" }
