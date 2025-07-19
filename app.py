import streamlit as st
import pandas as pd
from config import GOOGLE_SHEET_ID
from loaders import load_google_sheet
from filters import clean_and_filter, apply_manual_filters
from layout.onboarding_ui import render_welcome_panel
from layout.filters_ui import render_filter_panel
from layout.results_ui import render_results

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

    # 🧭 Get full list of agencies
    full_agency_list = pd.concat([
        df_star["Agency Name"],
        df_talent["Agency Name"]
    ]).dropna().unique().tolist()

    # 🌟 UI Filter — select one agency, optional
    selected_date, id1, id2, selected_agency = render_filter_panel(date_options, sorted(full_agency_list))

    # 🔄 Default view: Alpha + RCKLESS if no selection
    default_agencies = ["Alpha Agency", "RCKLESS"]
    active_agencies = [selected_agency] if selected_agency else default_agencies

    df_star_view = df_star[df_star["Agency Name"].isin(active_agencies)].copy()
    df_talent_view = df_talent[df_talent["Agency Name"].isin(active_agencies)].copy()

    # 📊 Final viewer output
    st.sidebar.info(f"📌 Viewing events for: {', '.join(active_agencies)}")
    render_results(df_star_view, df_talent_view)

if __name__ == "__main__":
    main()