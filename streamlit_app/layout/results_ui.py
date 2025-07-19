import streamlit as st
import pandas as pd
from filters import format_for_display
from config import DISPLAY_COLUMNS

def render_results(df_star, df_talent):
    st.subheader("📋 Star Task PK")
    df_star_disp = format_for_display(df_star, DISPLAY_COLUMNS)
    st.dataframe(df_star_disp)

    st.subheader("📋 Talent PK")
    df_talent_disp = format_for_display(df_talent, DISPLAY_COLUMNS)
    st.dataframe(df_talent_disp)

    combined = pd.concat([df_star_disp, df_talent_disp], ignore_index=True)
    combined["Source"] = (
        ["Star Task PK"] * len(df_star_disp) +
        ["Talent PK"] * len(df_talent_disp)
    )

    sort_columns = [c for c in ["Date", "PK Time"] if c in combined.columns]
    combined_sorted = combined.sort_values(by=sort_columns).reset_index(drop=True)

    st.subheader("📎 Combined Results – Chronological")
    st.dataframe(combined_sorted)

    if not combined_sorted.empty:
        csv = combined_sorted.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Combined CSV",
            data=csv,
            file_name="filtered_agency_events.csv",
            mime="text/csv"
        )