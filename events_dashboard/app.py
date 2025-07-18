import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import re

st.set_page_config(page_title="Agency Event Viewer", layout="wide")

# --- Load File or Prompt Upload ---
excel_path = Path("data/July_2025_UK_AgencyHost_Events.xlsx")
if not excel_path.exists():
    st.warning("Excel file not found. Please upload below:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if not uploaded_file:
        st.stop()
    xls = pd.ExcelFile(uploaded_file)
else:
    xls = pd.ExcelFile(excel_path)

# --- Detect Relevant Sheets Only ---
def is_relevant_sheet(sheet_name):
    try:
        preview = xls.parse(sheet_name, nrows=1)
        return any(col in preview.columns for col in ["Talent PK", "Star Task PK"])
    except:
        return False

relevant_sheets = [s for s in xls.sheet_names if is_relevant_sheet(s)]
sheet_options = ["ALL"] + relevant_sheets
selected_sheet = st.sidebar.selectbox("Select Sheet", sheet_options)

# --- Extract Columns from Sheet(s) ---
def extract_relevant(sheet_name):
    df = xls.parse(sheet_name)
    keep = [
        "Talent PK", "Star Task PK", "Agency Name", "ID 1", "ID 2",
        "Date", "Day", "PK Time"
    ]
    return df[[col for col in keep if col in df.columns]]

if selected_sheet == "ALL":
    df = pd.concat([extract_relevant(s) for s in relevant_sheets], ignore_index=True)
else:
    df = extract_relevant(selected_sheet)

# --- Filter for Alpha & RCKLESS ---
df = df[df["Agency Name"].isin(["Alpha", "RCKLESS"])]

# --- Format Date & Day ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
df["Day"] = pd.to_datetime(df["Day"], errors="coerce").dt.day_name()

# --- Format PK Time from 24hr → 12hr ---
def parse_pk_time(value):
    value = str(value).strip()
    if re.match(r"^\d{1,2}:\d{2}$", value):
        try:
            return pd.to_datetime(value, format="%H:%M").strftime("%I:%M %p")
        except:
            return "N/A"
    return "N/A"

if "PK Time" in df.columns:
    df["PK Time"] = df["PK Time"].apply(parse_pk_time)

# --- Viewer Filters ---
day = st.multiselect("Day", df["Day"].dropna().unique())
date = st.multiselect("Date", df["Date"].dropna().unique())
id1_input = st.text_input("Search by ID 1")
id2_input = st.text_input("Search by ID 2")

# --- Apply Filters ---
filtered_df = df.copy()
if day:
    filtered_df = filtered_df[filtered_df["Day"].isin(day)]
if date:
    filtered_df = filtered_df[filtered_df["Date"].isin(date)]
if id1_input:
    filtered_df = filtered_df[filtered_df["ID 1"].astype(str).str.contains(id1_input, case=False, na=False)]
if id2_input:
    filtered_df = filtered_df[filtered_df["ID 2"].astype(str).str.contains(id2_input, case=False, na=False)]

# --- Display Results ---
st.dataframe(filtered_df)

# --- Download Filtered Spreadsheet ---
def convert_df_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="📥 Download Filtered Results",
    data=convert_df_to_excel(filtered_df),
    file_name="filtered_events.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)