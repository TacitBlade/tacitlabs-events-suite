# layout/onboarding_ui.py
import streamlit as st

def render_welcome_panel():
    st.title("📊 Agency Event Dashboard")
    st.markdown("""
    Welcome to the UK Agency & Host Event Viewer — designed for talent teams, admins, and collaborators.

    #### What this dashboard does:
    - 📤 Automatically pull event data from a shared Google Sheet
    - 🔍 Filter events by date, ID, and agency
    - 📎 View Star & Talent results
    - ⬇️ Export filtered results

    ---
    #### Getting Started:
    Just open the app — it connects live to your data.
    """)
    st.info("ℹ️ This app fetches the latest agency data directly from Google Sheets.")
    st.divider()