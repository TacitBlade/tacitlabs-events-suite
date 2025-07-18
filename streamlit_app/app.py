import streamlit as st
from loaders import load_workbook
from filters import clean_and_filter, apply_manual_filters
from layout import render_filter_panel, render_results
from config import DEFAULT_AGENCIES, DISPLAY_COLUMNS

def main():
    st.set_page_config(page_title="Agency Event Filter", layout="wide")
    st.title("📊 UK Agency & Host Event Viewer")

    uploaded_file = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])
    if not uploaded_file:
        st.info("Upload your event workbook to begin.")
        return

    sheets = load_workbook(uploaded_file)
    df_star, df_talent, date_options = clean_and_filter(sheets, DEFAULT_AGENCIES)

    # ⏱️ User inputs
    selected_date, id1_input, id2_input = render_filter_panel(date_options)

    df_star_filtered   = apply_manual_filters(df_star, selected_date, id1_input, id2_input)
    df_talent_filtered = apply_manual_filters(df_talent, selected_date, id1_input, id2_input)

    render_results(df_star_filtered, df_talent_filtered)

if __name__ == "__main__":
    main()