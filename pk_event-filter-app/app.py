import streamlit as st
import pandas as pd
from utils.data_loader import load_data

st.set_page_config(page_title="Agency Filter Dashboard", layout="wide")
st.title("🎯 Star Tasks & Talent PK Overview")

def show_data_tab(sheet_name, label, tab_area):
    with tab_area:
        df, error = load_data(sheet_name)
        if not df.empty:
            agencies = df["Agency"].dropna().unique()
            selected = st.multiselect(f"Filter by Agency", agencies)
            filtered = df[df["Agency"].isin(selected)] if selected else df
            st.dataframe(filtered)
        else:
            st.warning(f"{label} sheet not found. Upload a file to proceed.")
            uploaded = st.file_uploader(f"Upload {label} Excel File", type=["xlsx"])
            if uploaded:
                df = pd.read_excel(uploaded)
                st.dataframe(df)

tab1, tab2 = st.tabs(["⭐ Star Tasks", "🎭 Talent PK"])
show_data_tab("Star Task PK", "Star Tasks", tab1)
show_data_tab("Talent PK", "Talent PK", tab2)