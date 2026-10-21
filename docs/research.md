# Investigación (octubre 2026)
Proyectos públicos evaluados. Las estrellas son aproximadas; revisar código antes de usar.

## MCP servers
| Repo | ★ | Uso |
|---|---|---|
| pauling-ai/youtube-mcp-server | ~28 | Data + Analytics + Reporting API, 40 tools (elegido: `youtube-studio`, fijado a v0.3.0 `ec13ee5`) |
| ZubeidHendricks/youtube-mcp-server | ~584 | Gestión de videos, Shorts, analítica (alternativa) |
| kimtaeyoon83/mcp-server-youtube-transcript | ~602 | Transcripciones (descartado: npm publica una 0.1.1 de 2024 y youtube-studio ya trae transcripciones) |
| jkawamoto/mcp-youtube-transcript | ~489 | Transcripciones (alternativa Python) |

## Skills / toolkits para creadores
| Repo | ★ | Nota |
|---|---|---|
| AgriciDaniel/claude-youtube | ~471 | Auditoría, SEO, guiones, miniaturas, monetización; base de inspiración |
| adityaarsharma/youtube-marketing-skills | ~60 | 21 comandos + MCP de canal |
| sergebulaev/youtube-skills, deeployCO/youtube-seo-skills, ahmedsakri/youtube-agent-pro | <60 | Pequeños; solo referencia |

## Automatización
| Repo | ★ | Nota |
|---|---|---|
| rushindrasinha/youtube-shorts-pipeline | ~2.3k | Pipeline completo de Shorts con IA (cuidado con políticas de contenido inauténtico) |
| SJbuilds04/yt-auto-uploader | ~24 | Programación multi-canal desde Drive |
| parafoxia/analytix | ~45 | SDK Python de YouTube Analytics |

## Plugins del catálogo de Claude
Marketing (Anthropic), TubeAlfred YouTube, Hyper Marketing, Windsor.ai. Instalar desde el marketplace si se necesita analítica/ads/SEO ampliados.

## Riesgos
Proyectos recientes y pequeños: auditar código y permisos OAuth (mínimo privilegio). No automatizar subidas masivas sin valor añadido.

## Skills de terceros instaladas
- `Jakeschincariol/youtube-agent-skill` (MIT), commit `a2feb21` (16 sep 2026): las 11 skills `yt-*` copiadas en `.claude/skills/`. Revisadas: los scripts de Python son locales, sin red ni dependencias. Cambio local: `hookscore.py` y `hooks.json` de `yt-script` ampliados con palabras y patrones en español (el original solo entendía inglés); `title.py` de `yt-package` acepta letras con acento al comparar título y miniatura; el resto se copió tal cual.
