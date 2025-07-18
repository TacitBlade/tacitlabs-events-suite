import streamlit as st
import pandas as pd
from utils import apply_filters

st.set_page_config(page_title="Agency Events Hub", page_icon="📊", layout="wide")

# Inject CSS styling
with open("branding.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Header
st.markdown('<h1>📊 July 2025 Agency Events Hub</h1>', unsafe_allow_html=True)
st.markdown("Upload event data, apply filters, and export results.")
st.markdown("---")

# Upload file
uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, sheet_name="Events")
    st.success("✅ File uploaded and loaded.")
else:
    st.warning("📁 Upload an Excel file to begin.")