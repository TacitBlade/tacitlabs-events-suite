import streamlit as st
import pandas as pd
from config import GOOGLE_SHEET_ID
from loaders import load_google_sheet
from utils.data_utils import combine_pk_events
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

    # 🧹 Combine and clean PK events
    combined_df = combine_pk_events(raw_sheets)

    # 🗂️ Sheet options for selector
    sheet_names = ["Combined PK Events"]

    # 🧭 Build agency list
    agency_list = combined_df["Agency Name"].dropna().unique().tolist()
    selected_sheet, selected_date, id1, id2, selected_agency = render_filter_panel(
        [],  # optional: populate date options later
        sorted(agency_list),
        sheet_names
    )

    # 📌 Default agencies if none selected
    default_agencies = ["Alpha Agency", "RCKLESS"]
    active_agency = selected_agency or default_agencies[0]

    # 🎯 Filter view
    df_view = combined_df[combined_df["Agency Name"] == active_agency].copy()

    st.sidebar.info(f"📌 Viewing events for: {active_agency}")
    render_results(df_view, pd.DataFrame())  # Only use one sheet viewer

if __name__ == "__main__":
    main()