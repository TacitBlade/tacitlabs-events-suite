import streamlit as st

def render_filter_panel(date_options):
    st.sidebar.header("🔍 Filter Controls")
    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        selected_date = st.date_input(
            label="Pick a Date – DD/MM/YYYY",
            value=None,
            min_value=min(date_options),
            max_value=max(date_options),
            format="DD/MM/YYYY"
        )
    with col2:
        id1_input = st.text_input("Filter by ID 1", "")
    with col3:
        id2_input = st.text_input("Filter by ID 2", "")

    return selected_date, id1_input, id2_input