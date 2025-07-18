import os
import streamlit as st
import pandas as pd
from utils import apply_filters
from config import APP_NAME, VERSION, CONTACT_EMAIL, AGENCY_URL

# ─── Page Config & Styling ───────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_NAME,
    page_icon="assets/favicon.ico",
    layout="wide"
)

st.image("assets/logo.png", width=120)

with open("branding.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    #logo
    st.image("assets/logo.png", width=120)

#session_state["theme"]
if st.toggle("🌙 Enable Dark Mode"):
    with open("dark.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
else:
    with open("branding.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ─── Welcome Card ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="
        background-color: #EEF2FC;
        padding: 20px;
        border-left: 5px solid #2E3A8C;
        border-radius: 10px;
        margin-bottom: 30px;
    ">
      <h3 style="margin-bottom:10px;">
        Welcome to the July 2025 Agency & Host Events Hub 🎉
      </h3>
      <p>
        Upload your Excel file to explore and filter events by date, time block,
        agency, or identifiers.
      </p>
      <ul>
        <li>🔍 Use filters to narrow by date, day, PK time, and ID</li>
        <li>📅 View event counts by date</li>
        <li>📥 Download filtered results instantly</li>
      </ul>
    </div>
    """,
    unsafe_allow_html=True
)

# ─── Data Loading ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader("📂 Upload Excel file", type=["xlsx"])
if uploaded_file is None:
    demo_path = os.path.join("sample_data", "demo.xlsx")
    df = pd.read_excel(demo_path, sheet_name="Events")
    st.info("No file uploaded. Using demo data for preview.")
else:
    df = pd.read_excel(uploaded_file, sheet_name="Events")
    st.success("✅ File uploaded and loaded.")

# ─── Tabs: Filtered View / Summary / Export ────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔎 Filtered View", "📅 Summary", "📥 Export"])

with tab1:
    st.subheader("🔍 Apply Filters")
    c1, c2, c3 = st.columns(3)
    with c1:
        date    = st.multiselect("Date",    sorted(df["Date"].dropna().unique()))
        day     = st.multiselect("Day",     sorted(df["Day"].dropna().unique()))
    with c2:
        pk_time = st.multiselect("PK Time", sorted(df["PK Time"].dropna().unique()))
        agency  = st.multiselect("Agency Name", sorted(df["Agency Name"].dropna().unique()))
    with c3:
        id1     = st.multiselect("ID 1", sorted(df["ID 1"].dropna().unique()))
        id2     = st.multiselect("ID 2", sorted(df["ID 2"].dropna().unique()))

    filtered_df = apply_filters(df, date, day, pk_time, agency, id1, id2)
    st.write(f"**Total Events:** {len(filtered_df)}")
    st.dataframe(filtered_df, use_container_width=True)

with tab2:
    st.subheader("📅 Events by Date")
    if not filtered_df.empty:
        summary = (
            filtered_df.groupby("Date")
            .agg(Event_Count=("Agency Name", "count"))
            .reset_index()
        )
        st.dataframe(summary, use_container_width=True)
    else:
        st.warning("No data to summarize. Adjust filters or upload a file.")

with tab3:
    st.subheader("📥 Export Filtered Results")
    if not filtered_df.empty:
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv_data, "Filtered_Events.csv", "text/csv")
    else:
        st.warning("No data to export. Adjust filters or upload a file.")

# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    f"""
    <div style="
        text-align:center;
        font-size:14px;
        color:#666;
        margin-top:20px;
    ">
        <p>📞 Contact: <strong>{CONTACT_EMAIL}</strong></p>
        <p>Version {VERSION} &nbsp; | &nbsp; Powered by <a href="{AGENCY_URL}" target="_blank">Tacit Labs</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
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