import streamlit as st
import pandas as pd

def load_workbook(uploaded_file):
    try:
        return pd.read_excel(uploaded_file, sheet_name=["Star Task PK", "Talent PK"])
    except ImportError:
        st.error("Missing Excel engine. Try: pip install openpyxl")
        st.stop()
    except ValueError as ve:
        st.error(f"Missing sheets: {ve}")
        st.stop()
    except Exception as e:
        st.error(f"Excel loading error: {e}")
        st.stop()