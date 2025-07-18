import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

st.set_page_config(page_title="Agency Event Viewer", layout="wide")

# --- Load Excel File or Prompt Upload ---
excel_path = Path("events_dashboard/assets/July 2025 UK Agency&Host Events .xlsx")
if not excel_path.exists():
    st.warning("No file found at expected path. Please upload your Excel file:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if uploaded_file:
        xls = pd.ExcelFile(uploaded_file)
    else:
        st.stop()  # Wait for upload
else:
    xls = pd.ExcelFile(excel_path)

# --- Sheet Selector ---
sheet_name = st.sidebar.selectbox("Select Sheet", xls.sheet_names)
df = xls.parse(sheet_name)

# --- Filter for Alpha & RCKLESS ---
df = df[df["Agency Name"].isin(["Alpha", "RCKLESS"])]

# --- Format Date & Time ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.date.astype(str)
df["PK Time"] = pd.to_datetime(df["PK Time"], errors="coerce").dt.strftime("%I:%M %p")

# --- Filters ---
day = st.multiselect("Day", df["Day"].dropna().unique())
id1 = st.multiselect("ID 1", df["ID 1"].dropna().unique())
id2 = st.multiselect("ID 2", df["ID 2"].dropna().unique())

filtered_df = df.copy()
if day: filtered_df = filtered_df[filtered_df["Day"].isin(day)]
if id1: filtered_df = filtered_df[filtered_df["ID 1"].isin(id1)]
if id2: filtered_df = filtered_df[filtered_df["ID 2"].isin(id2)]

# --- Display Data ---
st.dataframe(filtered_df)

# --- Export as Excel ---
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="📥 Download Filtered Results",
    data=convert_df_to_excel(filtered_df),
    file_name="filtered_events.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)