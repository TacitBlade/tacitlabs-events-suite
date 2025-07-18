import pandas as pd

def clean_and_filter(sheets: dict, agencies: list[str]):
    """
    Cleans both Star Task PK and Talent PK sheets:
    - Normalizes agency names (uppercase, stripped)
    - Filters by selected agencies
    - Converts 'Date' column to datetime
    - Returns both filtered DataFrames + available date options
    """
    normalized_agencies = [a.upper().strip() for a in agencies]

    def prepare(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        if "Agency Name" in df.columns:
            df["Agency Name"] = df["Agency Name"].astype(str).str.strip().str.upper()
            df = df[df["Agency Name"].isin(normalized_agencies)]
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df

    df_star = prepare(sheets.get("Star Task PK", pd.DataFrame()))
    df_talent = prepare(sheets.get("Talent PK", pd.DataFrame()))

    df_all = pd.concat([df_star, df_talent], ignore_index=True).dropna(subset=["Date"])
    available_dates = sorted(df_all["Date"].dt.date.unique())

    return df_star, df_talent, available_dates

def apply_manual_filters(df: pd.DataFrame, selected_date, id1_filter, id2_filter):
    """
    Applies filters for selected date, ID 1, and ID 2.
    Returns a cleaned and narrowed DataFrame.
    """
    if selected_date and "Date" in df.columns:
        df = df[df["Date"].dt.date == selected_date]
    if "ID 1" in df.columns and id1_filter:
        df = df[df["ID 1"].astype(str).str.contains(id1_filter, case=False, na=False)]
    if "ID 2" in df.columns and id2_filter:
        df = df[df["ID 2"].astype(str).str.contains(id2_filter, case=False, na=False)]
    return df

def format_for_display(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Returns a display-ready version of the DataFrame:
    - Subsets to desired columns
    - Formats date column as DD/MM/YYYY
    """
    df = df[[c for c in columns if c in df.columns]].copy()
    if "Date" in df.columns:
        df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")
    return df