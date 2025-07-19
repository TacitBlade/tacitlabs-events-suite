import streamlit as st
import pandas as pd

def load_workbook(uploaded_file):
    """Safely load required sheets from uploaded Excel file."""
    try:
        return pd.read_excel(uploaded_file, sheet_name=["Star Task PK", "Talent PK"])
    except ImportError:
        st.error("Missing engine. Try:\n\npip install openpyxl")
        st.stop()
    except ValueError as ve:
        st.error(f"Sheet error: {ve}")
        st.stop()
    except Exception as e:
        st.error(f"Excel loading error:\n\n{e}")
        st.stop()