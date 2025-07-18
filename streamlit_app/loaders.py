import streamlit as st
import pandas as pd

def load_workbook(uploaded_file):
    """Safely load required sheets from uploaded Excel file."""
    try:
        sheets = pd.read_excel(
            uploaded_file,
            sheet_name=["Star Task PK", "Talent PK"]
        )
        return sheets
    except ImportError:
        st.error("❌ `openpyxl` is missing. Please install:\n\n    pip install openpyxl\n\nThen restart.")
        st.stop()
    except ValueError as ve:
        st.error(f"Sheet error: {ve}")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error reading Excel file:\n\n{e}")
        st.stop()