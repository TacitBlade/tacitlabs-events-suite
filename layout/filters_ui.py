def render_filter_panel(date_options):
    import streamlit as st

    st.sidebar.header("🔍 Filter Controls")
    col1, col2, col3 = st.sidebar.columns(3)

    with col1:
        selected_date = st.date_input(
            "Pick a Date",
            value=None,
            min_value=min(date_options),
            max_value=max(date_options),
            format="DD/MM/YYYY"
        )
    with col2:
        id1 = st.text_input("Filter by ID 1", "")
    with col3:
        id2 = st.text_input("Filter by ID 2", "")

    return selected_date, id1, id2