# layout/results_ui.py
import streamlit as st
import pandas as pd

def render_results(df_star, df_talent):
    st.subheader("📅 Combined Event Viewer")

    # Combine sheets
    df_combined = pd.concat([df_star, df_talent], ignore_index=True)

    # 🧹 Strip time from 'Date', but keep time from 'PK Time'
    df_combined["Date"] = pd.to_datetime(df_combined["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    df_combined["Time"] = df_combined["PK Time"].astype(str)

    # 🧹 Trim to essential columns
    display_df = df_combined[["Date", "Time", "Agency Name"]].rename(
        columns={"Agency Name": "Agency"}
    ).sort_values(["Date", "Time"])

    st.dataframe(display_df, use_container_width=True)