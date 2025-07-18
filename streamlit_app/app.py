import streamlit as st
import pandas as pd

# Cache the workbook-loading for performance
@st.cache_data
def load_sheets(uploaded_file):
    try:
        # Try reading only the two relevant sheets
        return pd.read_excel(
            uploaded_file,
            sheet_name=["Star Task PK", "Talent PK"]
        )
    except ImportError:
        st.error(
            "It looks like the engine for reading .xlsx files is missing.\n\n"
            "Please install openpyxl:\n\n"
            "    pip install openpyxl\n\n"
            "Then restart the app."
        )
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error loading Excel file:\n\n{e}")
        st.stop()

def filter_by_agency(df: pd.DataFrame, agencies: list[str], agency_col="Agency") -> pd.DataFrame:
    """
    Return only rows where df[agency_col] is in agencies.
    If the column is missing, returns an empty DataFrame with the same columns.
    """
    if agency_col not in df.columns:
        return pd.DataFrame(columns=df.columns)
    mask = df[agency_col].isin(agencies)
    return df.loc[mask].reset_index(drop=True)

def main():
    st.set_page_config(page_title="Agency Filter App", layout="wide")
    st.title("✨ Star Task PK & Talent PK Agency Filter")
    st.write("""
        Upload your Excel workbook, then select which agencies to include
        from the **Star Task PK** and **Talent PK** sheets.
    """)

    uploaded_file = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])
    if not uploaded_file:
        st.info("Awaiting your Excel file upload…")
        return

    # Load sheets
    sheets = load_sheets(uploaded_file)

    # Build sidebar selections
    st.sidebar.header("Filter Options")
    agency_lists = [
        df["Agency"] for df in sheets.values() if "Agency" in df.columns
    ]
    all_agencies = (
        pd.concat(agency_lists, ignore_index=True)
          .dropna()
          .unique()
          .tolist()
    )

    selected_agencies = st.sidebar.multiselect(
        "Select agencies to include",
        options=all_agencies,
        default=["Alpha Agency", "Rckless"]
    )

    # Filter each sheet
    df_star   = filter_by_agency(sheets.get("Star Task PK", pd.DataFrame()), selected_agencies)
    df_talent = filter_by_agency(sheets.get("Talent PK",     pd.DataFrame()), selected_agencies)

    # Display results
    st.subheader("Star Task PK – Filtered")
    st.dataframe(df_star)

    st.subheader("Talent PK – Filtered")
    st.dataframe(df_talent)

    # Combine & download
    combined = pd.concat([
        df_star.assign(Source="Star Task PK"),
        df_talent.assign(Source="Talent PK")
    ], ignore_index=True)

    st.subheader("Combined Results")
    st.dataframe(combined)

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