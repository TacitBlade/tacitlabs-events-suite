import streamlit as st
import pandas as pd

from config import GOOGLE_SHEET_ID
from loaders import load_google_sheet
from utils.data_utils import combine_pk_events
from utils.filter_utils import filter_events
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

    selected_sheet, selected_agencies, id1, id2 = render_filter_panel(sheet_names, sorted(all_agencies))

    if not selected_agencies:
        selected_agencies = ["Alpha Agency", "RCKLESS"]

    if selected_sheet == "Star Task PK":
        filtered_df = filter_events(df_star, selected_agencies, id1, id2)
        render_results(filtered_df, pd.DataFrame())
    elif selected_sheet == "Talent PK":
        filtered_df = filter_events(df_talent, selected_agencies, id1, id2)
        render_results(pd.DataFrame(), filtered_df)
    else:
        filtered_df = filter_events(combined_df, selected_agencies, id1, id2)
        render_results(filtered_df, pd.DataFrame())

if __name__ == "__main__":
    main()