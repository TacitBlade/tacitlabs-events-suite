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
            "Pick a Date –,
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
    star_formatted = format_for_display(df_star, DISPLAY_COLUMNS)
    st.dataframe(star_formatted)

    st.subheader("📋 Talent PK")
    talent_formatted = format_for_display(df_talent, DISPLAY_COLUMNS)
    st.dataframe(talent_formatted)

    combined = pd.concat([star_formatted, talent_formatted], ignore_index=True)
    combined["Source"] = (
        ["Star Task PK"] * len(star_formatted) +
        ["Talent PK"] * len(talent_formatted)
    )

    sort_columns = [col for col in ["Date", "PK Time"] if col in combined.columns]
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