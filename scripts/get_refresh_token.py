"""Genera GOOGLE_REFRESH_TOKEN y lo guarda en .env (sin imprimirlo).

Requiere GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET en .env (cliente OAuth de
tipo "Aplicación de escritorio"). Abre el navegador para autorizar; si
administras un canal de marca, elige ese canal en la pantalla de Google.
Ver docs/setup-google-oauth.md.
"""
import argparse
import os

from dotenv import load_dotenv, set_key
from google_auth_oauthlib.flow import InstalledAppFlow

ENV_PATH = ".env"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
]
PUBLISH_SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--publish", action="store_true", help="incluye scopes para subir y editar videos")
    p.add_argument("--port", type=int, default=0, help="puerto local para el redirect (0 = aleatorio)")
    a = p.parse_args()

    if not os.path.exists(ENV_PATH):
        raise SystemExit("No existe .env: copia .env.example y completa GOOGLE_CLIENT_ID y GOOGLE_CLIENT_SECRET.")
    load_dotenv(ENV_PATH)
    client_id = os.environ.get("GOOGLE_CLIENT_ID")
    client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise SystemExit("Faltan GOOGLE_CLIENT_ID o GOOGLE_CLIENT_SECRET en .env.")

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        },
        scopes=SCOPES + (PUBLISH_SCOPES if a.publish else []),
    )
    # prompt=consent fuerza a Google a devolver un refresh token nuevo.
    creds = flow.run_local_server(port=a.port, access_type="offline", prompt="consent")
    if not creds.refresh_token:
        raise SystemExit("Google no devolvió refresh token. Revoca el acceso en myaccount.google.com/permissions y reintenta.")

    set_key(ENV_PATH, "GOOGLE_REFRESH_TOKEN", creds.refresh_token, quote_mode="never")
    print("Listo: GOOGLE_REFRESH_TOKEN guardado en .env.")


if __name__ == "__main__":
    main()
