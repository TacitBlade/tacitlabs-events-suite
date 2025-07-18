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

def filter_by_agency(df: pd.DataFrame, agencies: list[str], agency_col="Agency Name") -> pd.DataFrame:
    """
    Return only rows where df[agency_col] is in agencies.
    If the column is missing, returns an empty DataFrame with the same columns.
    """
    if agency_col not in df.columns:
        return pd.DataFrame(columns=df.columns)
    return df[df[agency_col].isin(agencies)].reset_index(drop=True)

def main():
    st.set_page_config(page_title="Agency Filter App", layout="wide")
    st.title("✨ Star Task PK & Talent PK Agency Filter")
    st.write(
        "Upload your Excel workbook and select agencies to include—filtering on “Agency Name.”\n\n"
        "Results show only Date, Day, PK Time, Agency Name, ID 1, ID 2."
    )

    uploaded_file = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])
    if not uploaded_file:
        st.info("Awaiting your Excel file upload…")
        return

    # Load sheets
    sheets = load_sheets(uploaded_file)

    # Sidebar: agency selector
    st.sidebar.header("Filter Options")
    agency_cols = [
        df["Agency Name"]
        for df in sheets.values()
        if isinstance(df, pd.DataFrame) and "Agency Name" in df.columns
    ]
    if agency_cols:
        all_agencies = (
            pd.concat(agency_cols, ignore_index=True)
              .dropna()
              .unique()
              .tolist()
        )
    else:
        all_agencies = []
        st.sidebar.warning("No 'Agency Name' column found.")

    selected_agencies = st.sidebar.multiselect(
        "Select agencies to include",
        options=all_agencies,
        default=[a for a in ["Alpha Agency", "Rckless"] if a in all_agencies]
    )

    # Filter each sheet
    df_star   = filter_by_agency(sheets.get("Star Task PK", pd.DataFrame()), selected_agencies)
    df_talent = filter_by_agency(sheets.get("Talent PK",    pd.DataFrame()), selected_agencies)

    # Columns to display
    cols_to_show = ["Date", "Day", "PK Time", "Agency Name", "ID 1", "ID 2"]

    def subset(df: pd.DataFrame) -> pd.DataFrame:
        return df[[c for c in cols_to_show if c in df.columns]]

    df_star_disp   = subset(df_star)
    df_talent_disp = subset(df_talent)

    # Display filtered sheets
    st.subheader("Star Task PK – Filtered")
    st.dataframe(df_star_disp)

    st.subheader("Talent PK – Filtered")
    st.dataframe(df_talent_disp)

    # Combine and display
    combined = pd.concat([df_star_disp, df_talent_disp], ignore_index=True)
    st.subheader("Combined Results")
    st.dataframe(combined)

    # Download button
    if not combined.empty:
        csv_bytes = combined.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download filtered data as CSV",
            data=csv_bytes,
            file_name="filtered_agencies.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()