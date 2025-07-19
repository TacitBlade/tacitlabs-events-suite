# loaders.py
import requests
import pandas as pd

def fetch_sheet_from_google(sheet_id: str, filename: str = "AgencyEvents.xlsx") -> str:
    export_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
    response = requests.get(export_url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    else:
        raise Exception(f"🚫 Failed to fetch sheet. Status code: {response.status_code}")

def load_google_sheet(sheet_id: str) -> dict:
    file_path = fetch_sheet_from_google(sheet_id)
    return pd.read_excel(file_path, sheet_name=["Star Task PK", "Talent PK"])