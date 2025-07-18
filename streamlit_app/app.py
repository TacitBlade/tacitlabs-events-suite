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

def filter_dataframe(df: pd.DataFrame, agencies: list[str]) -> pd.DataFrame:
    df = df[df["Agency Name"].isin(agencies)].copy()
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

def apply_filters(df: pd.DataFrame, selected_date, id1_filter, id2_filter):
    if selected_date:
        df = df[df["Date"].dt.date == selected_date]
    if "ID 1" in df.columns and id1_filter:
        df = df[df["ID 1"].astype(str).str.contains(id1_filter, case=False, na=False)]
    if "ID 2" in df.columns and id2_filter:
        df = df[df["ID 2"].astype(str).str.contains(id2_filter, case=False, na=False)]
    return df

def format_display(df: pd.DataFrame) -> pd.DataFrame:
    if "Date" in df.columns:
        df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")
    return df

def main():
    st.set_page_config(page_title="Agency Filter App", layout="wide")
    st.title("✨ Star Task PK & Talent PK Filter")
    st.write(
        "Upload your Excel workbook to filter event data by:\n"
        "- Agencies: Alpha Agency & Rckless\n"
        "- Calendar picker for Date (DD/MM/YYYY)\n"
        "- Manual filters for ID 1 and ID 2\n"
        "- Columns shown: Date, PK Time, Agency Name, ID 1, Agency Name(1), ID 2"
    )

    uploaded_file = st.file_uploader("Upload Excel workbook (.xlsx)", type=["xlsx"])
    if not uploaded_file:
        st.info("Awaiting your Excel file upload…")
        return

    sheets = load_sheets(uploaded_file)
    agencies = ["Alpha Agency", "Rckless Only"]
    columns_to_display = ["Date", "PK Time", "Agency Name", "ID 1", "Agency Name(1)", "ID 2"]

    def prepare(df: pd.DataFrame):
        if df.empty:
            return pd.DataFrame(columns=columns_to_display)
        df = filter_dataframe(df, agencies)
        return df[[c for c in columns_to_display if c in df.columns]]

    df_star = prepare(sheets.get("Star Task PK", pd.DataFrame()))
    df_talent = prepare(sheets.get("Talent PK", pd.DataFrame()))
    df_all = pd.concat([df_star, df_talent], ignore_index=True)
    df_all = df_all.dropna(subset=["Date"])
    available_dates = sorted(df_all["Date"].dt.date.unique())

    st.subheader("🔍 Filters")
    col1, col2, col3 = st.columns(3)
    with col1:
        selected_date = st.date_input(
            "Select Date (DD/MM/YYYY)",
            value=None,
            min_value=min(available_dates),
            max_value=max(available_dates),
            format="DD/MM/YYYY"
        )
    with col2:
        id1_input = st.text_input("Filter by ID 1", "")
    with col3:
        id2_input = st.text_input("Filter by ID 2", "")

    df_star_filtered = apply_filters(df_star, selected_date, id1_input, id2_input)
    df_talent_filtered = apply_filters(df_talent, selected_date, id1_input, id2_input)

    df_star_display = format_display(df_star_filtered)
    df_talent_display = format_display(df_talent_filtered)

    st.subheader("📋 Star Task PK – Results")
    st.dataframe(df_star_display)

    st.subheader("📋 Talent PK – Results")
    st.dataframe(df_talent_display)

    combined = pd.concat([df_star_display, df_talent_display], ignore_index=True)
    st.subheader("📎 Combined Results")
    st.dataframe(combined)

    if not combined.empty:
        csv_bytes = combined.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Combined CSV",
            data=csv_bytes,
            file_name="filtered_agency_data.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()