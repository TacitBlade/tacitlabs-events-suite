import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

st.set_page_config(page_title="Agency Event Viewer", layout="wide")

# --- Load File or Uploader ---
excel_path = Path("data/July_2025_UK_AgencyHost_Events.xlsx")
if not excel_path.exists():
    st.warning("Excel file not found. Please upload your file:")
    uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])
    if not uploaded_file:
        st.stop()
    xls = pd.ExcelFile(uploaded_file)
else:
    xls = pd.ExcelFile(excel_path)

# --- Select Sheet ---
sheet_name = st.sidebar.selectbox("Select Sheet", xls.sheet_names)
df = xls.parse(sheet_name)

# --- Filter for Agencies Only ---
df = df[df["Agency Name"].isin(["Alpha", "RCKLESS"])]

# --- Clean & Format Columns ---
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
df["Day"] = pd.to_datetime(df["Day"], errors="coerce").dt.day_name()
df["PK Time"] = pd.to_datetime(df["PK Time"], errors="coerce").dt.strftime("%I:%M %p")
df["PK Time"] = df["PK Time"].fillna("")

# --- Remove Unwanted Columns ---
columns_to_remove = [
    "UID 1", "UID 2", "PK POINT", "PK POINT.1", "Result", "Result.1",
    "Reward", "Reward.1", "Note", "Theme"
]
unnamed_cols = [col for col in df.columns if "Unnamed" in str(col)]
df.drop(columns=columns_to_remove + unnamed_cols, inplace=True, errors="ignore")

# --- Viewer Filters ---
day = st.multiselect("Day", df["Day"].dropna().unique())
date = st.multiselect("Date", df["Date"].dropna().unique())
id1 = st.multiselect("ID 1", df["ID 1"].dropna().unique())
id2 = st.multiselect("ID 2", df["ID 2"].dropna().unique())

# --- Apply Filters ---
filtered_df = df.copy()
if day:
    filtered_df = filtered_df[filtered_df["Day"].isin(day)]
if date:
    filtered_df = filtered_df[filtered_df["Date"].isin(date)]
if id1:
    filtered_df = filtered_df[filtered_df["ID 1"].isin(id1)]
if id2:
    filtered_df = filtered_df[filtered_df["ID 2"].isin(id2)]

# --- Display Filtered Data ---
st.dataframe(filtered_df)

# --- Download Filtered Results ---
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