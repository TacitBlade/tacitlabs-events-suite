# layout/results_ui.py
import streamlit as st
import pandas as pd

# 👥 Optional: preload a mapping of IDs to agency names
id_to_agency = {
    "A123": "Alpha Agency",
    "RK456": "RCKLESS",
    "X789": "Other Agency",
    # Add more ID-agency pairs here as needed
}

def _format_view(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Format date + time
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    df["Time"] = df["PK Time"].astype(str)

    # Agency for host (ID 1)
    df["Agency.1"] = df["Agency Name"].fillna("Unknown")

    # Agency for opponent (ID 2)
    df["Agency.2"] = df["ID 2"].map(id_to_agency).fillna("Unknown")

    # Final display columns
    return df[["Date", "Time", "ID 1", "Agency.1", "ID 2", "Agency.2"]].sort_values(["Date", "Time"]).reset_index(drop=True)

def render_results(df_star, df_talent):
    st.subheader("⭐ Star Task PK Viewer")
    st.dataframe(_format_view(df_star), use_container_width=True)

    st.subheader("🎯 Talent PK Viewer")
    st.dataframe(_format_view(df_talent), use_container_width=True)

    st.subheader("📋 Combined Event Viewer")
    combined_df = pd.concat([df_star, df_talent], ignore_index=True)
    st.dataframe(_format_view(combined_df), use_container_width=True)