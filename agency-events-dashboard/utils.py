def apply_filters(df, date=None, agency=None):
    if date:
        df = df[df["Date"].isin(date)]
    if agency:
        df = df[df["Agency Name"].isin(agency)]
    return df