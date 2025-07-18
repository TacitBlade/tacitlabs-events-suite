def apply_filters(df, date=None, day=None, pk_time=None, agency=None, id1=None, id2=None):
    if date:
        df = df[df["Date"].isin(date)]
    if day:
        df = df[df["Day"].isin(day)]
    if pk_time:
        df = df[df["PK Time"].isin(pk_time)]
    if agency:
        df = df[df["Agency Name"].isin(agency)]
    if id1:
        df = df[df["ID 1"].isin(id1)]
    if id2:
        df = df[df["ID 2"].isin(id2)]
    return df