import streamlit as st
import pandas as pd

@st.cache_data
def load_sheets(uploaded_file):
    try:
        return pd.read_excel(
            uploaded_file,
            sheet_name=["Star Task PK", "Talent PK"]
        )
    except ImportError:
        st.error("Missing engine for .xlsx files. Please install:\n\n    pip install openpyxl\n\nThen restart.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading Excel file:\n\n{e}")
        st.stop()

def filter_dataframe(df: pd.DataFrame, agency_list: list[str]) -> pd.DataFrame:
    """Filter by Agency Name and format Date."""
    df = df[df["Agency Name"].isin(agency_list)].copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    return df

def main():
    st.set_page_config(page_title="Agency Filter App", layout="wide")
    st.title("✨ Star Task PK & Talent PK Agency Filter")
    st.write(
        "Upload your Excel workbook to filter Star Task PK and Talent PK by:\n"
        "- Agency Name (Alpha Agency and Rckless)\n"
        "- Manual input filters for Date, ID 1, and ID 2"
    )

    uploaded_file = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])
    if not uploaded_file:
        st.info("Awaiting your Excel file upload…")
        return

    # Load sheets
    sheets = load_sheets(uploaded_file)
    selected_agencies = ["Alpha Agency", "Rckless"]

    # Display columns
    display_cols = ["Date", "PK Time", "Agency Name", "ID 1", "Agency Name(1)", "ID 2"]

    def prepare(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=display_cols)
        df = filter_dataframe(df, selected_agencies)
        return df[[col for col in display_cols if col in df.columns]]

    df_star   = prepare(sheets.get("Star Task PK", pd.DataFrame()))
    df_talent = prepare(sheets.get("Talent PK",    pd.DataFrame()))

    st.subheader("🔍 Text Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        date_filter = st.text_input("Filter by Date (e.g. 20/07/2025)", "")
    with col2:
        id1_filter = st.text_input("Filter by ID 1", "")
    with col3:
        id2_filter = st.text_input("Filter by ID 2", "")

    def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
        if date_filter:
            df = df[df["Date"].astype(str).str.contains(date_filter, case=False, na=False)]
        if id1_filter and "ID 1" in df.columns:
            df = df[df["ID 1"].astype(str).str.contains(id1_filter, case=False, na=False)]
        if id2_filter and "ID 2" in df.columns:
            df = df[df["ID 2"].astype(str).str.contains(id2_filter, case=False, na=False)]
        return df

    df_star_filtered   = apply_filters(df_star)
    df_talent_filtered = apply_filters(df_talent)

    st.subheader("📋 Star Task PK – Results")
    st.dataframe(df_star_filtered)

    st.subheader("📋 Talent PK – Results")
    st.dataframe(df_talent_filtered)

    combined = pd.concat([df_star_filtered, df_talent_filtered], ignore_index=True)
    st.subheader("📎 Combined Results")
    st.dataframe(combined)

    if not combined.empty:
        csv_bytes = combined.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download combined CSV",
            data=csv_bytes,
            file_name="filtered_agency_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()