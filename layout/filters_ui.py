import streamlit as st

def render_filter_panel(date_options, agency_list):
    st.sidebar.header("🔍 Filter Controls")

    if date_options:
        selected_date = st.sidebar.date_input(
            "Date",
            value=None,
            min_value=min(date_options),
            max_value=max(date_options),
            format="DD/MM/YYYY"
        )
    else:
        st.sidebar.warning("📅 No valid dates found in sheet.")
        selected_date = None

    col1, col2 = st.sidebar.columns(2)
    with col1:
        id1 = st.text_input("ID 1", "")
    with col2:
        id2 = st.text_input("ID 2", "")

    selected_agency = st.sidebar.selectbox("Agency", sorted(agency_list))
    return selected_date, id1, id2, selected_agency