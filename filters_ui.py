import pandas as pd

def clean_and_filter(sheets: dict, agencies: list[str]):
    normalized = [a.upper().strip() for a in agencies]

    def prep(df: pd.DataFrame):
        df = df.copy()
        if "Agency Name" in df.columns:
            df["Agency Name"] = df["Agency Name"].astype(str).str.upper().str.strip()
            df = df[df["Agency Name"].isin(normalized)]
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
        return df

    df_star = prep(sheets.get("Star Task PK", pd.DataFrame()))
    df_talent = prep(sheets.get("Talent PK", pd.DataFrame()))
    merged = pd.concat([df_star, df_talent], ignore_index=True).dropna(subset=["Date"])
    available_dates = sorted(merged["Date"].dt.date.unique())

    return df_star, df_talent, available_dates

def apply_manual_filters(df, selected_date, id1, id2):
    if selected_date and "Date" in df.columns:
        df = df[df["Date"].dt.date == selected_date]
    if "ID 1" in df.columns and id1:
        df = df[df["ID 1"].astype(str).str.contains(id1, case=False, na=False)]
    if "ID 2" in df.columns and id2:
        df = df[df["ID 2"].astype(str).str.contains(id2, case=False, na=False)]
    return df

def format_for_display(df, columns: list[str]):
    df = df[[c for c in columns if c in df.columns]].copy()
    if "Date" in df.columns:
        df["Date"] = df["Date"].dt.strftime("%d/%m/%Y")
    return df