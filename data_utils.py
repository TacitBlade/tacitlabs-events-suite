# utils/data_utils.py
import pandas as pd

def combine_pk_events(raw_sheets: dict) -> pd.DataFrame:
    # Safely load sheets
    df_star = raw_sheets.get("Star Task PK", pd.DataFrame()).copy()
    df_talent = raw_sheets.get("Talent PK", pd.DataFrame()).copy()

    # Concatenate both sheets
    combined_df = pd.concat([df_star, df_talent], ignore_index=True)

    # ⛔ Filter out rows containing metadata, rules, sign-up, etc.
    exclude_keywords = ["rules", "reward", "sign up", "sign-up", "registration", "note"]
    combined_df = combined_df[~combined_df.apply(
        lambda row: row.astype(str).str.lower().str.contains('|'.join(exclude_keywords)).any(), axis=1
    )]

    # 🧠 Create Event Date column (optional, if needed elsewhere)
    if "Date" in combined_df.columns and "PK Time" in combined_df.columns:
        combined_df["Event Date"] = pd.to_datetime(
            combined_df["Date"].astype(str) + " " + combined_df["PK Time"].astype(str),
            errors="coerce"
        )

    return combined_df.reset_index(drop=True)