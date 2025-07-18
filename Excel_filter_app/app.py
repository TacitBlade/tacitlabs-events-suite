import pandas as pd
import streamlit as st
from io import BytesIO

st.set_page_config(page_title="Excel Filter", layout="wide")
st.title("Excel Sheets Filter")

uploaded = st.file_uploader("Upload Excel file", type=["xlsx"])
if uploaded:
    xls = pd.ExcelFile(uploaded)
    sheet = st.selectbox("Choose sheet", xls.sheet_names)
    df = pd.read_excel(uploaded, sheet_name=sheet)

    # Normalize Date column
    df["Date"] = pd.to_datetime(df["Date"]).dt.date

    # Layout filters
    col1, col2 = st.columns(2)
    with col1:
        date_range = st.date_input(
            "Date range",
            value=(df["Date"].min(), df["Date"].max())
        )
        days = st.multiselect("Day", df["Day"].unique(), default=df["Day"].unique())
    with col2:
        pk_times = st.multiselect("PK Time", df["PK Time"].unique(), default=df["PK Time"].unique())
        agencies = st.multiselect("Agency Name", df["Agency Name"].unique(), default=df["Agency Name"].unique())
        id1 = st.multiselect("ID 1", df["ID 1"].unique(), default=df["ID 1"].unique())
        id2 = st.multiselect("ID 2", df["ID 2"].unique(), default=df["ID 2"].unique())

    # Apply filters
    mask = (
        (df["Date"] >= date_range[0]) &
        (df["Date"] <= date_range[1]) &
        (df["Day"].isin(days)) &
        (df["PK Time"].isin(pk_times)) &
        (df["Agency Name"].isin(agencies)) &
        (df["ID 1"].isin(id1)) &
        (df["ID 2"].isin(id2))
    )
    filtered = df[mask]
    st.dataframe(filtered)

    # Prepare download
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        filtered.to_excel(writer, sheet_name=sheet, index=False)
    buffer.seek(0)

    st.download_button(
        "Download filtered Excel",
        data=buffer,
        file_name=f"filtered_{sheet}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )