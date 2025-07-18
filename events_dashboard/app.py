import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO
import re

st.set_page_config(page_title="Agency Event Viewer", layout="wide")

# --- Load Excel File or Uploader ---
excel_path = Path("data/July_2025_UK_AgencyHost_Events.xlsx")
if not excel_path.exists():
    st.warning("Excel file not found. Please upload below:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if not uploaded_file:
        st.stop()
    xls = pd.ExcelFile(uploaded_file)
else:
    xls = pd.ExcelFile(excel_path)

# --- Sheet Selector with "ALL" Option ---
sheet_options = ["ALL"] + xls.sheet_names
selected_sheet = st.sidebar.selectbox("Select Sheet", sheet_options)

if selected_sheet == "ALL":
    df = pd.concat([xls.parse(name) for name in xls.sheet_names], ignore_index=True)
else:
    df = xls.parse(selected_sheet)

# --- Filter by Agency ---
df = df[df["Agency Name"].isin(["Alpha", "RCKLESS"])]

# --- Format Date and Day ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
df["Day"] = pd.to_datetime(df["Day"], errors="coerce").dt.day_name()

# --- Parse and Format PK Time from 24hr to 12hr ---
def parse_pk_time(value):
    value = str(value).strip()
    if re.match(r"^\d{1,2}:\d{2}$", value):
        try:
            return pd.to_datetime(value, format="%H:%M").strftime("%I:%M %p")
        except:
            return "N/A"
    return "N/A"

df["PK Time"] = df["PK Time"].apply(parse_pk_time)

# --- Remove Unwanted Columns ---
columns_to_remove = [
    "UID 1", "UID 2", "PK POINT", "PK POINT.1", "Result", "Result.1",
    "Reward", "Reward.1", "Note", "Theme"
]
unnamed_cols = [col for col in df.columns if "Unnamed" in str(col)]
df.drop(columns=columns_to_remove + unnamed_cols, inplace=True, errors="ignore")

# --- Add "All PK Points" per Agency from All Sheets ---
pk_agg = []
for name in xls.sheet_names:
    sheet_df = xls.parse(name)
    sheet_df["Agency Name"] = sheet_df["Agency Name"].astype(str)
    sheet_df["PK POINT"] = pd.to_numeric(sheet_df.get("PK POINT"), errors="coerce")
    filtered = sheet_df[sheet_df["Agency Name"].isin(["Alpha", "RCKLESS"])]
    pk_total = filtered.groupby("Agency Name")["PK POINT"].sum().reset_index()
    pk_agg.append(pk_total)
pk_summary = pd.concat(pk_agg, ignore_index=True).groupby("Agency Name").sum().reset_index()
pk_summary.rename(columns={"PK POINT": "All PK Points"}, inplace=True)
df = df.merge(pk_summary, on="Agency Name", how="left")

# --- Filtering UI ---
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

# --- Display Data ---
st.dataframe(filtered_df)

# --- Download Button ---
def convert_df_to_excel(dataframe):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        dataframe.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="📥 Download Filtered Events",
    data=convert_df_to_excel(filtered_df),
    file_name="filtered_events.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)