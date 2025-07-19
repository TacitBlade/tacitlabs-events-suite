# layout/onboarding_ui.py
import streamlit as st

def render_welcome_panel():
    st.title("📊 Agency Event Dashboard")
    st.markdown("""
    Welcome to the UK Agency & Host Event Viewer — designed for talent teams, admins, and collaborators.

    #### What this dashboard does:
    - 📤 Upload Excel event data
    - 🔍 Apply filters by date and ID
    - 📎 View results for Star + Talent
    - ⬇️ Download filtered results as CSV

    ---
    #### Getting Started:
    1. Prepare your `.xlsx` workbook with correct sheet names:
       - `Star Task PK`
       - `Talent PK`
    2. Launch the app — it pulls the sheet automatically
    3. Use the sidebar to filter by date, ID 1, or ID 2
    """)

    st.info("ℹ️ This app supports automated downloads from Google Sheets.")
    st.divider()