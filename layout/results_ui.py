# layout/results_ui.py
import streamlit as st

def render_results(df_star, df_talent):
    st.subheader("⭐ Star Task Results")
    st.dataframe(df_star, use_container_width=True)

    st.subheader("🎯 Talent PK Results")
    st.dataframe(df_talent, use_container_width=True)