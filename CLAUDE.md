# Gestión de canales de YouTube

Proyecto para administrar varios canales y maximizar monetización.

## Reglas
- Cada canal vive en `channels/<slug>/` (copiar `channels/_template`).
- Antes de proponer contenido, leer `channel.yaml` y `strategy.md` del canal.
- Nunca publicar, borrar ni modificar videos sin confirmación explícita del usuario.
- Nunca leer ni imprimir credenciales (`.env`, `client_secret*.json`, tokens).
- Cumplir políticas de YouTube: evitar contenido reutilizado/masivo sin valor añadido (riesgo para el YPP), marcar contenido patrocinado y sintético cuando aplique.
- Basar recomendaciones en datos de `data/` o del MCP `youtube-studio`; indicar qué es dato y qué es hipótesis.

## Skills
channel-audit, video-seo, script-retention, thumbnail-brief, shorts-repurpose, monetization-report, content-calendar.

Skills de terceros (`youtube-agent-skill`, ver `docs/research.md`): yt-audit, yt-chapters, yt-comment, yt-edit, yt-package, yt-plan, yt-retention, yt-script, yt-seo, yt-shorts, yt-viral. Se solapan con las anteriores (audit, seo, shorts, calendario, guion): preferir las propias para estrategia y monetización del proyecto, y las `yt-*` para lo que no cubren (capítulos, edición, retención, comentarios, viral). Sus scripts `.py` requieren Python 3.
