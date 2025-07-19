# layout/results_ui.py
import streamlit as st
import pandas as pd

def _format_view(df: pd.DataFrame, label: str) -> pd.DataFrame:
    # Clean date + time fields
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    df["Time"] = df["PK Time"].astype(str)
    df["Agency"] = df["Agency Name"].fillna("Unknown")

    # Trim to essential view
    return df[["Date", "Time", "Agency"]].sort_values(["Date", "Time"]).reset_index(drop=True)

def render_results(df_star, df_talent):
    st.subheader("⭐ Star Task PK Viewer")
    df_star_view = _format_view(df_star, "Star")
    st.dataframe(df_star_view, use_container_width=True)

    st.subheader("🎯 Talent PK Viewer")
    df_talent_view = _format_view(df_talent, "Talent")
    st.dataframe(df_talent_view, use_container_width=True)

    st.subheader("📋 Combined Event Viewer")
    df_combined = pd.concat([df_star_view, df_talent_view], ignore_index=True)
    st.dataframe(df_combined.sort_values(["Date", "Time"]).reset_index(drop=True), use_container_width=True)