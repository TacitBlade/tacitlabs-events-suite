def render_results(df_star, df_talent):
    import pandas as pd
    import streamlit as st

    def _format_view(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%d/%m/%Y")
        df["Time"] = df["PK Time"].astype(str)
        df["Agency"] = df["Agency Name"].fillna("Unknown")
        return df[["Date", "Time", "Agency"]].sort_values(["Date", "Time"]).reset_index(drop=True)

    st.subheader("⭐ Star Task PK Viewer")
    st.dataframe(_format_view(df_star), use_container_width=True)

    st.subheader("🎯 Talent PK Viewer")
    st.dataframe(_format_view(df_talent), use_container_width=True)

    st.subheader("📋 Combined Event Viewer")
    combined_df = pd.concat([df_star, df_talent], ignore_index=True)
    st.dataframe(_format_view(combined_df), use_container_width=True)