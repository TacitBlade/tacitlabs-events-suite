import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="PK Event Filter", layout="wide", page_icon="📑")
st.title("Talent PK & Star Task PK Filter")

uploaded = st.file_uploader("Upload Excel file", type="xlsx")
if uploaded:
    xls = pd.ExcelFile(uploaded)
    sheets = [s for s in xls.sheet_names if s in ["Talent PK", "Star Task PK"]]
    selected_sheet