# Genera episodes/epNN/{episode.md,queue.json} y queue/all_episodes.json desde episodes.json.
# base_settings.json debe reflejar los ajustes exportados de la UI de Wan2GP (Save settings).
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$utf8 = New-Object System.Text.UTF8Encoding($false)
$data = Get-Content (Join-Path $root 'episodes.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$base = Get-Content (Join-Path $root 'base_settings.json') -Raw -Encoding UTF8 | ConvertFrom-Json
New-Item -ItemType Directory -Force (Join-Path $root 'queue') | Out-Null
$all = @()
$n = 0
foreach ($ep in $data.episodes) {
    $n++
    $dir = Join-Path $root "episodes\$($ep.id)"
    New-Item -ItemType Directory -Force $dir | Out-Null
    $tasks = @(); $s = 0
    $md = "# $($ep.id) - $($ep.title)`n`nMoraleja: $($ep.moral)`n`nNegative prompt (todas las escenas): ``$($data.negative)```n"
    foreach ($scene in $ep.scenes) {
        $s++
        $text = $scene
        foreach ($c in $data.characters.PSObject.Properties) { $text = $text.Replace("{$($c.Name)}", $c.Value) }
        $prompt = "$($data.style) $text"
        $t = [ordered]@{}
        foreach ($p in $base.PSObject.Properties) { $t[$p.Name] = $p.Value }
        $t['prompt'] = $prompt
        $t['negative_prompt'] = $data.negative
        $t['seed'] = $n * 100 + $s
        $tasks += [pscustomobject]$t
        $md += "`n## Escena $s`n`n$prompt`n"
    }
    [IO.File]::WriteAllText((Join-Path $dir 'episode.md'), $md, $utf8)
    [IO.File]::WriteAllText((Join-Path $dir 'queue.json'), (ConvertTo-Json -InputObject $tasks -Depth 6), $utf8)
    $all += $tasks
}
[IO.File]::WriteAllText((Join-Path $root 'queue\all_episodes.json'), (ConvertTo-Json -InputObject $all -Depth 6), $utf8)
Write-Host "OK: $n episodios, $($all.Count) escenas"
