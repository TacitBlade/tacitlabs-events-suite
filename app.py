# app.py
import streamlit as st
import layout.onboarding_ui
print(dir(layout.onboarding_ui))


from config import GOOGLE_SHEET_ID, DEFAULT_AGENCIES
from loaders import load_google_sheet
from filters import clean_and_filter, apply_manual_filters, format_for_display
from layout.onboarding_ui import render_welcome_panel
from layout.filters_ui import render_filter_panel
from layout.results_ui import render_results

def main():
    st.set_page_config(page_title="Agency Event Viewer", layout="wide")

    render_welcome_panel()  # Intro panel
    st.sidebar.success("✅ Live sheet connected via Google Sheets")

    try:
        raw_sheets = load_google_sheet(GOOGLE_SHEET_ID)
    except Exception as e:
        st.error(f"📡 Unable to fetch sheet: {e}")
        return

    df_star, df_talent, date_options = clean_and_filter(raw_sheets, DEFAULT_AGENCIES)
    selected_date, id1, id2 = render_filter_panel(date_options)

    df_filtered_star = apply_manual_filters(df_star, selected_date, id1, id2)
    df_filtered_talent = apply_manual_filters(df_talent, selected_date, id1, id2)

    render_results(df_filtered_star, df_filtered_talent)

if __name__ == "__main__":
    main()