import streamlit as st
import pandas as pd
from pathlib import Path

# Load Excel File
excel_path = Path("data/July_2025_UK_AgencyHost_Events.xlsx")
xls = pd.ExcelFile(excel_path)

# Sidebar for Sheet Selection
sheet_name = st.sidebar.selectbox("Select Sheet", xls.sheet_names)

df = xls.parse(sheet_name)

# Filters
date = st.multiselect("Date", df["Date"].dropna().unique())
day = st.multiselect("Day", df["Day"].dropna().unique())
pk_time = st.multiselect("PK Time", df["PK Time"].dropna().unique())
agency = st.multiselect("Agency Name", df["Agency Name"].dropna().unique())
id1 = st.multiselect("ID 1", df["ID 1"].dropna().unique())
id2 = st.multiselect("ID 2", df["ID 2"].dropna().unique())

# Apply Filters
filtered_df = df.copy()
if date: filtered_df = filtered_df[filtered_df["Date"].isin(date)]
if day: filtered_df = filtered_df[filtered_df["Day"].isin(day)]
if pk_time: filtered_df = filtered_df[filtered_df["PK Time"].isin(pk_time)]
if agency: filtered_df = filtered_df[filtered_df["Agency Name"].isin(agency)]
if id1: filtered_df = filtered_df[filtered_df["ID 1"].isin(id1)]
if id2: filtered_df = filtered_df[filtered_df["ID 2"].isin(id2)]

st.dataframe(filtered_df)

# Download as Excel
def convert_df_to_excel(df):
    from io import BytesIO
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