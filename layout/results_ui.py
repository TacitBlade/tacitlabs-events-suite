import streamlit as st
import pandas as pd

def _format_view(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    df["Time"] = df["PK Time"].astype(str)
    df["Agency.1"] = df["Agency Name"].fillna("Unknown")
    df["ID 1"] = df.get("ID 1", "")
    df["ID 2"] = df.get("ID 2", "")

    id_to_agency = df.dropna(subset=["ID 1", "Agency Name"]).set_index("ID 1")["Agency Name"].to_dict()
    df["Agency.2"] = df["ID 2"].map(id_to_agency).fillna("Unknown")

    return df[["Date", "Time", "ID 1", "Agency.1", "ID 2", "Agency.2"]].sort_values(["Date", "Time"]).reset_index(drop=True)

def render_download(df: pd.DataFrame):
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download filtered results",
        data=csv,
        file_name="filtered_events.csv",
        mime="text/csv"
    )

def render_results(df_main, _unused):
    if not df_main.empty:
        st.subheader("📋 PK Event Viewer")
        formatted_df = _format_view(df_main)
        st.dataframe(formatted_df, use_container_width=True)
        render_download(formatted_df)