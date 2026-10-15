# Configurar credenciales de Google
1. Google Cloud Console → crea un proyecto.
2. Habilita **YouTube Data API v3**, **YouTube Analytics API** y **YouTube Reporting API**.
3. Credenciales → ID de cliente OAuth (aplicación de escritorio). Añade tu cuenta como usuario de prueba.
4. Scopes: `youtube.readonly`, `yt-analytics.readonly`, `yt-analytics-monetary.readonly` (añade `youtube.upload` / `youtube.force-ssl` solo si vas a publicar).
5. Obtén un refresh token con el flujo OAuth y guarda `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REFRESH_TOKEN` en `.env` (nunca en git).
6. `YOUTUBE_API_KEY` solo para lecturas públicas.
Cada canal de marca requiere autorizar su cuenta; el token da acceso al canal elegido.
