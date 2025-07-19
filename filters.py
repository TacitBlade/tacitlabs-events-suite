# filters.py
import pandas as pd

def clean_and_filter(raw_sheets: dict, agency_fallback: list):
    df_star = raw_sheets["Star Task PK"].copy()
    df_talent = raw_sheets["Talent PK"].copy()

    for df in [df_star, df_talent]:
        df["Event Date"] = pd.to_datetime(df["Event Date"], errors="coerce")
        df["Agency Name"] = df["Agency Name"].fillna("Unknown")

    date_options = sorted(df_star["Event Date"].dropna().dt.date.unique())

    return df_star, df_talent, date_options

def apply_manual_filters(df, date=None, id1=None, id2=None, agency=None):
    if date:
        df = df[df["Event Date"].dt.date == date]
    if id1:
        df = df[df["ID 1"] == id1]
    if id2:
        df = df[df["ID 2"] == id2]
    if agency and agency != "All Agencies":
        df = df[df["Agency Name"] == agency]
    return df