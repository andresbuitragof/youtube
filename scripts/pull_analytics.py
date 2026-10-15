"""Descarga métricas diarias de YouTube Analytics a data/<canal>_<inicio>_<fin>.csv.

Requiere credenciales OAuth en .env (ver docs/setup-google-oauth.md).
"""
import argparse
import os

import pandas as pd
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

METRICS = "views,estimatedMinutesWatched,averageViewDuration,subscribersGained,estimatedRevenue,cpm"


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--start", required=True)
    p.add_argument("--end", required=True)
    p.add_argument("--channel", default="MINE")
    a = p.parse_args()

    load_dotenv()
    creds = Credentials(
        None,
        refresh_token=os.environ["GOOGLE_REFRESH_TOKEN"],
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
    )
    creds.refresh(Request())
    yta = build("youtubeAnalytics", "v2", credentials=creds)
    ids = "channel==MINE" if a.channel == "MINE" else f"channel=={a.channel}"
    r = yta.reports().query(
        ids=ids, startDate=a.start, endDate=a.end, metrics=METRICS, dimensions="day", sort="day"
    ).execute()
    df = pd.DataFrame(r.get("rows", []), columns=[c["name"] for c in r["columnHeaders"]])
    out = f"data/{a.channel}_{a.start}_{a.end}.csv"
    df.to_csv(out, index=False)
    print(f"{len(df)} filas -> {out}")


if __name__ == "__main__":
    main()
