import pandas as pd
import streamlit as st

def clean_and_filter(raw_sheets: dict, agency_fallback: list):
    df_star = raw_sheets["Star Task PK"].copy()
    df_talent = raw_sheets["Talent PK"].copy()

    for df_name, df in zip(["Star", "Talent"], [df_star, df_talent]):
        # ⚠️ Check for presence of 'Date' and 'PK Time' columns
        if "Date" in df.columns and "PK Time" in df.columns:
            df["Event Date"] = pd.to_datetime(
                df["Date"].astype(str) + " " + df["PK Time"].astype(str),
                errors="coerce"
            )
        else:
            st.sidebar.error(f"⚠️ '{df_name}' sheet missing 'Date' or 'PK Time' column")
            df["Event Date"] = pd.NaT  # fallback

        # 🔄 Clean Agency column
        if "Agency Name" in df.columns:
            df["Agency Name"] = df["Agency Name"].fillna("Unknown")
        else:
            st.sidebar.error(f"⚠️ '{df_name}' sheet missing 'Agency Name' column")
            df["Agency Name"] = "Unknown"

    date_options = sorted(df_star["Event Date"].dropna().dt.date.unique())
    return df_star, df_talent, date_options

def apply_manual_filters(df, date=None, id1=None, id2=None, agency=None):
    # 🧹 Apply filters only if columns exist
    if "Event Date" in df.columns and date:
        df = df[df["Event Date"].dt.date == date]
    if id1 and "ID 1" in df.columns:
        df = df[df["ID 1"] == id1]
    if id2 and "ID 2" in df.columns:
        df = df[df["ID 2"] == id2]
    if "Agency Name" in df.columns and agency and agency != "All Agencies":
        df = df[df["Agency Name"] == agency]
    return df