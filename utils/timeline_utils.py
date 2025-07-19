from datetime import datetime, timedelta
import pandas as pd

def filter_by_days(df: pd.DataFrame, days: int) -> pd.DataFrame:
    if "Event Date" not in df.columns:
        return df
    cutoff = datetime.now() - timedelta(days=days)
    return df[df["Event Date"] >= cutoff]