# Configurar credenciales de Google
1. Google Cloud Console → crea un proyecto.
2. Habilita **YouTube Data API v3**, **YouTube Analytics API** y **YouTube Reporting API**.
3. Credenciales → ID de cliente OAuth (aplicación de escritorio). Añade tu cuenta como usuario de prueba.
4. Scopes: `youtube.readonly`, `yt-analytics.readonly`, `yt-analytics-monetary.readonly` (añade `youtube.upload` / `youtube.force-ssl` solo si vas a publicar).
5. Guarda `GOOGLE_CLIENT_ID` y `GOOGLE_CLIENT_SECRET` en `.env` (nunca en git) y ejecuta `python scripts/get_refresh_token.py` (añade `--publish` si vas a publicar). Abre el navegador, autorizas con la cuenta del canal y el script escribe `GOOGLE_REFRESH_TOKEN` en `.env` sin mostrarlo.
6. `YOUTUBE_API_KEY` solo para lecturas públicas.
Mientras la app esté en modo "Prueba" en la pantalla de consentimiento, Google caduca el refresh token a los 7 días; pásala a "En producción" para evitarlo (para uso personal no requiere verificación).

Cada canal de marca requiere autorizar su cuenta; el token da acceso al canal elegido.
