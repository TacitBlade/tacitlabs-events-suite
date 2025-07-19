import pandas as pd

def filter_events(df: pd.DataFrame, selected_agencies: list, id1: str, id2: str) -> pd.DataFrame:
    df = df.copy()

    if selected_agencies:
        df = df[df["Agency Name"].isin(selected_agencies)]

    if id1:
        df = df[df["ID 1"].astype(str).str.contains(id1, case=False)]

    if id2:
        df = df[df["ID 2"].astype(str).str.contains(id2, case=False)]

    return df.reset_index(drop=True)