import streamlit as st
import pandas as pd

# Cache the workbook-loading for performance
@st.cache_data
def load_sheets(uploaded_file):
    try:
        return pd.read_excel(
            uploaded_file,
            sheet_name=["Star Task PK", "Talent PK"]
        )
    except ImportError:
        st.error(
            "Missing engine for .xlsx files. Install with:\n\n"
            "    pip install openpyxl\n\n"
            "and restart."
        )
        st.stop()
    except Exception as e:
        st.error(f"Error loading Excel file:\n\n{e}")
        st.stop()

def filter_dataframe(df: pd.DataFrame, selected_agencies: list[str]) -> pd.DataFrame:
    """Filter by Agency Name and format Date."""
    df = df[df["Agency Name"].isin(selected_agencies)].copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
    return df

def main():
    st.set_page_config(page_title="Agency Filter App", layout="wide")
    st.title("✨ Star Task PK & Talent PK Agency Filter")
    st.write(
        "Upload your Excel workbook to filter Star Task PK and Talent PK sheets by:\n"
        "- Agency Name (only Alpha Agency and Rckless)\n"
        "- No dropdowns—use native Streamlit filters below\n"
        "- Display columns: Date, PK Time, Agency Name, ID 1, Agency Name(1), ID 2"
    )

    uploaded_file = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])
    if not uploaded_file:
        st.info("Awaiting your Excel file upload…")
        return

    # Load sheets
    sheets = load_sheets(uploaded_file)

    # Hard-coded filter for agencies
    selected_agencies = ["Alpha Agency", "Rckless"]

    # Define final column set
    display_columns = ["Date", "PK Time", "Agency Name", "ID 1", "Agency Name(1)", "ID 2"]

    def prep(df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return pd.DataFrame(columns=display_columns)
        df = filter_dataframe(df, selected_agencies)
        df = df[[col for col in display_columns if col in df.columns]]
        return df

    df_star   = prep(sheets.get("Star Task PK", pd.DataFrame()))
    df_talent = prep(sheets.get("Talent PK",    pd.DataFrame()))

    # Native filters (no dropdowns)
    st.subheader("🔍 Apply Data Filters")

    def apply_native_filters(df: pd.DataFrame, label: str) -> pd.DataFrame:
        if df.empty:
            st.warning(f"No data available in {label} after filtering.")
            return df

        # Apply column filters directly
        col1, col2, col3 = st.columns(3)
        with col1:
            day_filter = st.text_input(f"{label} — Filter by Day (e.g. Monday)", "")
        with col2:
            id1_filter = st.text_input(f"{label} — Filter by ID 1", "")
        with col3:
            id2_filter = st.text_input(f"{label} — Filter by ID 2", "")

        if "Day" in df.columns and day_filter:
            df = df[df["Day"].astype(str).str.contains(day_filter, case=False, na=False)]
        if "ID 1" in df.columns and id1_filter:
            df = df[df["ID 1"].astype(str).str.contains(id1_filter, case=False, na=False)]
        if "ID 2" in df.columns and id2_filter:
            df = df[df["ID 2"].astype(str).str.contains(id2_filter, case=False, na=False)]
        return df

    df_star_filtered   = apply_native_filters(df_star, "Star Task PK")
    df_talent_filtered = apply_native_filters(df_talent, "Talent PK")

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