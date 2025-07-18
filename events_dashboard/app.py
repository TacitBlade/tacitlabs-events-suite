import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import re

st.set_page_config(page_title="Agency Event Viewer", layout="wide")

# --- File Load / Uploader ---
excel_path = Path("data/July_2025_UK_AgencyHost_Events.xlsx")
if not excel_path.exists():
    st.warning("Excel file not found. Please upload below:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if not uploaded_file:
        st.stop()
    xls = pd.ExcelFile(uploaded_file)
else:
    xls = pd.ExcelFile(excel_path)

# --- Sheet Selector with 'ALL' ---
sheet_options = ["ALL"] + xls.sheet_names
selected_sheet = st.sidebar.selectbox("Select Sheet", sheet_options)

# --- Extract Relevant Columns Only ---
def extract_relevant(sheet):
    expected = [
        "Talent PK", "Star Task PK", "Agency Name", "ID 1", "ID 2",
        "Date", "Day", "PK Time"
    ]
    available = [col for col in expected if col in sheet.columns]
    return sheet[available]

if selected_sheet == "ALL":
    df = pd.concat([extract_relevant(xls.parse(name)) for name in xls.sheet_names], ignore_index=True)
else:
    df = extract_relevant(xls.parse(selected_sheet))

# --- Filter for Alpha & RCKLESS Only ---
df = df[df["Agency Name"].isin(["Alpha", "RCKLESS"])]

# --- Format Date & Day ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
df["Day"] = pd.to_datetime(df["Day"], errors="coerce").dt.day_name()

# --- Parse 24-Hour PK Time to 12-Hour ---
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

# --- Filter Inputs ---
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

# --- Display Filtered Data ---
st.dataframe(filtered_df)

# --- Excel Download ---
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