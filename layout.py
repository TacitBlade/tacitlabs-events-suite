import streamlit as st
import pandas as pd
from filters import format_for_display
from config import DISPLAY_COLUMNS

def render_filter_panel(date_options):
    """Renders calendar picker and manual ID filters."""
    st.sidebar.header("🔍 Filter Controls")
    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        selected_date = st.date_input(
            label="Pick a Date",  # ✅ Brackets removed
            value=None,
            min_value=min(date_options),
            max_value=max(date_options),
            format="DD/MM/YYYY"
        )
    with col2:
        id1_input = st.text_input("Filter by ID 1", "")
    with col3:
        id2_input = st.text_input("Filter by ID 2", "")

    return selected_date, id1_input, id2_input

def render_results(df_star, df_talent):
    """Displays both sheets and a sorted, merged table."""
    st.subheader("📋 Star Task PK")
    df_star_formatted = format_for_display(df_star, DISPLAY_COLUMNS)
    st.dataframe(df_star_formatted)

    st.subheader("📋 Talent PK")
    df_talent_formatted = format_for_display(df_talent, DISPLAY_COLUMNS)
    st.dataframe(df_talent_formatted)

    # Combine with source tags
    combined = pd.concat([df_star_formatted, df_talent_formatted], ignore_index=True)
    combined["Source"] = (
        ["Star Task PK"] * len(df_star_formatted) +
        ["Talent PK"] * len(df_talent_formatted)
    )

    # Chronological sort
    sort_keys = [key for key in ["Date", "PK Time"] if key in combined.columns]
    combined_sorted = combined.sort_values(by=sort_keys).reset_index(drop=True)

    st.subheader("📎 Combined Results – Chronological")
    st.dataframe(combined_sorted)

    # Download
    if not combined_sorted.empty:
        csv_bytes = combined_sorted.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Combined CSV",
            data=csv_bytes,
            file_name="filtered_agency_events.csv",
            mime="text/csv"
        )