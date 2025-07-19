import streamlit as st

def render_filter_panel(date_options, agency_list, sheet_names):
    st.sidebar.header("🔍 Filter Controls")

    selected_sheet = st.sidebar.selectbox("Sheet", sheet_names)

    col1, col2 = st.sidebar.columns(2)
    with col1:
        id1 = st.text_input("ID 1", "")
    with col2:
        id2 = st.text_input("ID 2", "")

    selected_agency = st.sidebar.selectbox("Agency", agency_list)
    return selected_sheet, None, id1, id2, selected_agency