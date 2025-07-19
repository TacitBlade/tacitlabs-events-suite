import streamlit as st

def render_filter_panel(sheet_names, agency_list):
    st.sidebar.header("🔍 Filter Controls")

    selected_sheet = st.sidebar.selectbox("Sheet", sheet_names)
    selected_agencies = st.sidebar.multiselect("Agencies", agency_list)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        id1 = st.text_input("ID 1")
    with col2:
        id2 = st.text_input("ID 2")

    selected_range = st.sidebar.selectbox("Date Range", ["All", "Last 7 days", "Last 30 days", "Last 90 days"])

    return selected_sheet, selected_agencies, id1, id2, selected_range