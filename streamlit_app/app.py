import streamlit as st
import pandas as pd

# 1. Cache the data-loading step for performance
@st.cache_data
def load_sheets(uploaded_file):
    # Read both sheets into a dict of DataFrames
    sheets = pd.read_excel(
        uploaded_file,
        sheet_name=["Star Task PK", "Talent PK"]
    )
    return sheets

# 2. Filter function for agencies
def filter_by_agency(df, agencies, agency_column="Agency"):
    # Retain only rows where the agency column matches one of the selected agencies
    mask = df[agency_column].isin(agencies)
    return df.loc[mask].reset_index(drop=True)

def main():
    st.set_page_config(
        page_title="Agency Filter App",
        layout="wide"
    )

    st.title("✨ Star Task PK & Talent PK Agency Filter")
    st.write(
        """
        Upload your Excel file, then select which agencies you want to see
        from the Star Task PK and Talent PK sheets.
        """
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Upload your Excel workbook",
        type=["xlsx"]
    )
    if not uploaded_file:
        st.info("Please upload the Excel file to get started.")
        return

    # Load data
    sheets = load_sheets(uploaded_file)

    # Sidebar selectors
    st.sidebar.header("Filter Options")
    # Automatically detect unique agencies across both sheets
    all_agencies = pd.concat(
        [df["Agency"] for df in sheets.values()]
    ).dropna().unique().tolist()

    selected_agencies = st.sidebar.multiselect(
        "Select agencies to include",
        options=all_agencies,
        default=["Alpha Agency", "Rckless"]
    )

    # Apply filters
    filtered_star = filter_by_agency(
        sheets["Star Task PK"], selected_agencies
    )
    filtered_talent = filter_by_agency(
        sheets["Talent PK"], selected_agencies
    )

    # Display results
    st.subheader("Star Task PK – Filtered")
    st.dataframe(filtered_star)

    st.subheader("Talent PK – Filtered")
    st.dataframe(filtered_talent)

    # Combine and offer download
    combined = pd.concat(
        [filtered_star.assign(Source="Star Task PK"),
         filtered_talent.assign(Source="Talent PK")],
        ignore_index=True
    )
    st.subheader("Combined Results")
    st.dataframe(combined)

    csv = combined.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download filtered data as CSV",
        data=csv,
        file_name="filtered_agencies.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()