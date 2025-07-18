import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import re

st.set_page_config(page_title="Talent & Star Task Viewer", layout="wide")

# --- File load or uploader fallback ---
excel_path = Path("data/July_2025_UK_AgencyHost_Events.xlsx")
if not excel_path.exists():
    st.warning("Excel file not found. Please upload below:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if not uploaded_file:
        st.stop()
    xls = pd.ExcelFile(uploaded_file)
else:
    xls = pd.ExcelFile