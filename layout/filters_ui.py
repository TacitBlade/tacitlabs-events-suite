import streamlit as st

def render_filter_panel(date_options, agency_list):
    st.sidebar.header("🔍 Filter Controls")

    # 🧠 Safely handle empty date options
    if date_options:
        selected_date = st.sidebar.date_input(
            "Pick a Date – DD/MM/YYYY",
            value=None,
            min_value=min(date_options),
            max_value=max(date_options),
            format="DD/MM/YYYY"
        )
    else:
        st.sidebar.warning("📅 No valid dates found in sheet.")
        selected_date = None

    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        id1 = st.text_input("Filter by ID 1", "")
    with col2:
        id2 = st.text_input("Filter by ID 2", "")
    with col3:
        selected_agency = st.selectbox(
            "🏢 Select Agency", ["All Agencies"] + sorted(agency_list)
        )

    return selected_date, id1, id2, selected_agency