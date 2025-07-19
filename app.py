import streamlit as st
import pandas as pd
from config import GOOGLE_SHEET_ID
from loaders import load_google_sheet
from utils.data_utils import combine_pk_events
from utils.filter_utils import filter_events
from utils.timeline_utils import filter_by_days
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

    combined_df, df_star, df_talent = combine_pk_events(raw_sheets)

    sheet_names = ["Combined PK Events", "Star Task PK", "Talent PK"]
    all_agencies = pd.concat([
        combined_df["Agency Name"],
        df_star["Agency Name"],
        df_talent["Agency Name"]
    ]).dropna().unique().tolist()

    selected_sheet, selected_agencies, id1, id2, selected_range = render_filter_panel(sheet_names, sorted(all_agencies))

    if not selected_agencies:
        selected_agencies = ["Alpha Agency", "RCKLESS"]

    if selected_sheet == "Star Task PK":
        df_view = filter_events(df_star, selected_agencies, id1, id2)
    elif selected_sheet == "Talent PK":
        df_view = filter_events(df_talent, selected_agencies, id1, id2)
    else:
        df_view = filter_events(combined_df, selected_agencies, id1, id2)

    # ⏳ Apply timeline filter
    if selected_range != "All":
        day_map = {
            "Last 7 days": 7,
            "Last 30 days": 30,
            "Last 90 days": 90
        }
        days = day_map.get(selected_range, 0)
        df_view = filter_by_days(df_view, days)

    render_results(df_view, pd.DataFrame())

if __name__ == "__main__":
    main()