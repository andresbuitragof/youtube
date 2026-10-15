# YouTube Channels Manager

Estructura base para gestionar y monetizar canales de YouTube con Claude Code.

## Inicio rápido
1. `cp .env.example .env` y completa credenciales (ver `docs/setup-google-oauth.md`).
2. `pip install -r scripts/requirements.txt`
3. `cp -r channels/_template channels/mi-canal` y edita `channel.yaml`.
4. Abre Claude Code aquí: usa `/channel-audit`, `/video-seo`, `/script-retention`, `/thumbnail-brief`, `/shorts-repurpose`, `/monetization-report`, `/content-calendar`.
5. Analítica: `python scripts/pull_analytics.py --start 2026-01-01 --end 2026-01-31`.

Investigación de proyectos, skills y plugins: `docs/research.md`.
