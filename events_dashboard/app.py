import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import re

st.set_page_config(page_title="Talent & Star Task Viewer", layout="wide")

# --- Load File or Prompt for Upload ---
excel_path = Path("events_dashboard/assets/July 2025 UK Agency&Host Events .xlsx")
if not excel_path.exists():
    st.warning("Excel file not found. Please upload below:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if not uploaded_file:
        st.stop()
    xls = pd.ExcelFile(uploaded_file)
else:
    xls = pd.ExcelFile(excel_path)

# --- Define Target Sheets ---
target_sheets = ["Talent", "Star Task"]
available_sheets = [s for s in target_sheets if s in xls.sheet_names]

if not available_sheets:
    st.error("No 'Talent' or 'Star Task' sheets found.")
    st.stop()

# --- Columns to Keep ---
columns_to_extract = ["Date", "PK Time", "Agency Name", "ID 1", "ID 2"]

# --- Load + Filter from Relevant Sheets ---
def load_sheet(sheet_name):
    df = xls.parse(sheet_name)
    df = df[[col for col in columns_to_extract if col in df.columns]]
    return df[df["Agency Name"].isin(["Alpha", "RCKLESS"])]

df = pd.concat([load_sheet(name) for name in available_sheets], ignore_index=True)

# --- Format Date & Add Day ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Day"] = df["Date"].dt.day_name()
df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")

# --- Format PK Time from 24hr to 12hr ---
def format_pk_time(value):
    value = str(value).strip()
    if re.match(r"^\d{1,2}:\d{2}$", value):
        try:
            return pd.to_datetime(value, format="%H:%M").strftime("%I:%M %p")
        except:
            return "N/A"
    return "N/A"

if "PK Time" in df.columns:
    df["PK Time"] = df["PK Time"].apply(format_pk_time)

# --- Filters ---
day = st.multiselect("Day", df["Day"].dropna().unique())
date = st.multiselect("Date", df["Date"].dropna().unique())
id1 = st.text_input("Search by ID 1")
id2 = st.text_input("Search by ID 2")

# --- Apply Filters ---
filtered_df = df.copy()
if day:
    filtered_df = filtered_df[filtered_df["Day"].isin(day)]
if date:
    filtered_df = filtered_df[filtered_df["Date"].isin(date)]
if id1:
    filtered_df = filtered_df[filtered_df["ID 1"].astype(str).str.contains(id1, case=False, na=False)]
if id2:
    filtered_df = filtered_df[filtered_df["ID 2"].astype(str).str.contains(id2, case=False, na=False)]

# --- Display Results ---
st.dataframe(filtered_df)

# --- Download Filtered Data ---
def convert_df_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="📥 Download Filtered Events",
    data=convert_df_to_excel(filtered_df),
    file_name="filtered_talent_star_task.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)