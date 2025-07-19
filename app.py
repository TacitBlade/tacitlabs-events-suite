# app.py
import streamlit as st
from config import GOOGLE_SHEET_ID
from loaders import load_google_sheet
from filters import clean_and_filter, apply_manual_filters
from layout.onboarding_ui import render_welcome_panel
from layout.filters_ui import render_filter_panel
from layout.results_ui import render_results
import pandas as pd

def main():
    st.set_page_config(page_title="Agency Event Viewer", layout="wide")
    render_welcome_panel()

    try:
        raw_sheets = load_google_sheet(GOOGLE_SHEET_ID)
        st.sidebar.success("✅ Connected to live Google Sheet")
    except Exception as e:
        st.error(f"📡 Sheet download failed: {e}")
        return

    df_star, df_talent, date_options = clean_and_filter(raw_sheets, [])
    agency_list = pd.concat([df_star["Agency Name"], df_talent["Agency Name"]]).dropna().unique().tolist()

    selected_date, id1, id2, selected_agency = render_filter_panel(date_options, agency_list)

    df_filtered_star = apply_manual_filters(df_star, selected_date, id1, id2, selected_agency)
    df_filtered_talent = apply_manual_filters(df_talent, selected_date, id1, id2, selected_agency)

    render_results(df_filtered_star, df_filtered_talent)

if __name__ == "__main__":
    main()