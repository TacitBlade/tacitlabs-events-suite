# layout/results_ui.py
import streamlit as st
import pandas as pd

def _format_view(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ⏱ Format date + time
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    df["Time"] = df["PK Time"].astype(str)

    # 🏢 Host agency
    df["Agency.1"] = df["Agency Name"].fillna("Unknown")

    # 🧠 Build live ID-to-agency map from all ID 1 / Agency Name pairs
    id_agency_map = df.dropna(subset=["ID 1", "Agency Name"]).set_index("ID 1")["Agency Name"].to_dict()

    # 🏢 Opponent agency
    df["Agency.2"] = df["ID 2"].map(id_agency_map).fillna("Unknown")

    return df[["Date", "Time", "ID 1", "Agency.1", "ID 2", "Agency.2"]].sort_values(["Date", "Time"]).reset_index(drop=True)

def render_results(df_star, df_talent):
    st.subheader("⭐ Star Task PK Viewer")
    st.dataframe(_format_view(df_star), use_container_width=True)

    st.subheader("🎯 Talent PK Viewer")
    st.dataframe(_format_view(df_talent), use_container_width=True)

    st.subheader("📋 Combined Event Viewer")
    combined_df = pd.concat([df_star, df_talent], ignore_index=True)
    st.dataframe(_format_view(combined_df), use_container_width=True)