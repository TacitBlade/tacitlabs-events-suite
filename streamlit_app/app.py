import streamlit as st
import pandas as pd
from pandas.errors import MissingOptionalDependency

# Cache the workbook-loading for performance
@st.cache_data
def load_sheets(uploaded_file):
    try:
        # Read only the two relevant sheets
        sheets = pd.read_excel(
            uploaded_file,
            sheet_name=["Star Task PK", "Talent PK"]
        )
        return sheets
    except MissingOptionalDependency:
        st.error(
            "The ‘openpyxl’ engine is required to read .xlsx files.\n\n"
            "Please install it with:\n\n"
            "    pip install openpyxl\n\n"
            "Then restart the app."
        )
        st.stop()

def filter_by_agency(df: pd.DataFrame, agencies: list[str], agency_column="Agency") -> pd.DataFrame:
    """
    Return only rows where df[agency_column] is in agencies.
    If the column is missing, returns an empty DataFrame.
    """
    if agency_column not in df.columns:
        return pd.DataFrame(columns=df.columns)
    mask = df[agency_column].isin(agencies)
    return df.loc[mask].reset_index(drop=True)

def main():
    st.set_page_config(
        page_title="Agency Filter App",
        layout="wide"
    )

    st.title("✨ Star Task PK & Talent PK Agency Filter")
    st.write(
        "Upload your Excel workbook and select which agencies to include\n"
        "from the Star Task PK and Talent PK sheets."
    )

    uploaded_file = st.file_uploader(
        label="Upload Excel workbook (.xlsx)",
        type=["xlsx"]
    )
    if not uploaded_file:
        st.info("Please upload the Excel file to get started.")
        return

    # Load both sheets
    sheets = load_sheets(uploaded_file)

    # Build sidebar selector
    st.sidebar.header("Filter Options")
    # Gather all agencies present in either sheet
    all_agencies = pd.concat(
        [
            df["Agency"] 
            for df in sheets.values() 
            if "Agency" in df.columns
        ],
        ignore_index=True
    ).dropna().unique().tolist()

    selected_agencies = st.sidebar.multiselect(
        label="Select agencies to include",
        options=all_agencies,
        default=["Alpha Agency", "Rckless"]
    )

    # Apply filters
    df_star = filter_by_agency(sheets.get("Star Task PK", pd.DataFrame()), selected_agencies)
    df_talent = filter_by_agency(sheets.get("Talent PK", pd.DataFrame()), selected_agencies)

    # Display each sheet
    st.subheader("Star Task PK – Filtered")
    st.dataframe(df_star)

    st.subheader("Talent PK – Filtered")
    st.dataframe(df_talent)

    # Combine and offer download
    combined = pd.concat(
        [
            df_star.assign(Source="Star Task PK"),
            df_talent.assign(Source="Talent PK")
        ],
        ignore_index=True
    )

    st.subheader("Combined Results")
    st.dataframe(combined)

    if not combined.empty:
        csv = combined.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download filtered data as CSV",
            data=csv,
            file_name="filtered_agencies.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()