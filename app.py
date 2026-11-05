import os
import pandas as pd
import streamlit as st
from modules.ingestion import load_dataset
from modules.profiling import profile_dataset
from modules.cleaning import clean_dataset
from modules.validation import assess_quality
from modules.analytics import build_analytics
from modules.visualisations import render_visualisations
from modules.recommendations import generate_recommendations
from modules.reporting import make_excel_report, make_text_report

st.set_page_config(page_title="DataFlow Intelligence", page_icon="📊", layout="wide")
st.title("📊 DataFlow Intelligence")
st.caption("Created by Philip Okposo | Naijadataman")
st.write("Clean, validate, and analyze data for clearer insights.")

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Upload CSV or Excel", type=["csv","xlsx","xls"])
    sample = st.checkbox("Use the included sample sales dataset")
    if uploaded is not None:
        st.session_state["source_bytes"] = uploaded.getvalue()
        st.session_state["source_name"] = uploaded.name
    elif sample:
        sample_path = os.path.join(os.path.dirname(__file__), "sample_data", "sample_sales_data.csv")
        with open(sample_path, "rb") as f:
            st.session_state["source_bytes"] = f.read()
        st.session_state["source_name"] = "sample_sales_data.csv"

if "source_bytes" not in st.session_state:
    st.info("Upload a CSV/Excel file or select the sample dataset in the sidebar to begin.")
    st.markdown("""
    **Workflow:** Ingest → Profile → Clean → Validate → Analyse → Recommend → Report

    The application keeps the original data unchanged and processes a separate working copy.
    """)
    st.stop()

source_signature = (st.session_state["source_name"], hash(st.session_state["source_bytes"]))
if st.session_state.get("active_source_signature") != source_signature:
    for key in ("cleaned_data", "audit", "raw_data"):
        st.session_state.pop(key, None)
    st.session_state["active_source_signature"] = source_signature

try:
    raw = load_dataset(st.session_state["source_bytes"], st.session_state["source_name"])
except Exception as e:
    st.error(f"Could not read this file: {e}")
    st.stop()

st.subheader("1. Source data")
a,b,c = st.columns(3)
a.metric("Rows", f"{len(raw):,}")
b.metric("Columns", f"{len(raw.columns):,}")
c.metric("Duplicate rows", f"{int(raw.duplicated().sum()):,}")
st.dataframe(raw.head(20), use_container_width=True)

with st.expander("Initial data profile", expanded=True):
    st.dataframe(profile_dataset(raw), use_container_width=True)

st.subheader("2. ETL cleaning studio")
st.write("Choose the operations to apply. The source dataset above remains unchanged.")
with st.form("cleaning_options"):
    c1,c2,c3 = st.columns(3)
    remove_duplicates = c1.checkbox("Remove duplicate rows", True)
    trim_text = c2.checkbox("Trim text spaces", True)
    standardise_text = c3.checkbox("Collapse repeated spaces", True)
    drop_empty_cols = c1.checkbox("Remove completely empty columns", True)
    infer_types = c2.checkbox("Convert likely numeric/date columns", True)
    missing_strategy = c3.selectbox("Missing-value strategy", ["Keep as missing","Drop rows with missing values","Fill numeric with median","Fill numeric with mean","Fill with mode"])
    submitted = st.form_submit_button("Run ETL process", type="primary")
if submitted or "cleaned_data" not in st.session_state:
    cleaned, audit = clean_dataset(raw, remove_duplicates=remove_duplicates, trim_text=trim_text,
        standardise_text=standardise_text, drop_empty_cols=drop_empty_cols, infer_types=infer_types,
        missing_strategy=missing_strategy)
    st.session_state["cleaned_data"] = cleaned
    st.session_state["audit"] = audit
    st.session_state["raw_data"] = raw.copy()

cleaned = st.session_state["cleaned_data"]
audit = st.session_state["audit"]
st.subheader("3. Cleaning results")
x,y,z = st.columns(3)
x.metric("Rows after cleaning", f"{len(cleaned):,}", delta=f"{len(cleaned)-len(raw):,} vs source")
y.metric("Columns after cleaning", f"{len(cleaned.columns):,}", delta=f"{len(cleaned.columns)-len(raw.columns):,} vs source")
z.metric("Missing cells remaining", f"{int(cleaned.isna().sum().sum()):,}")
st.dataframe(cleaned.head(20), use_container_width=True)
st.markdown("**ETL audit log**")
if audit:
    st.dataframe(pd.DataFrame(audit), use_container_width=True)
else:
    st.success("No cleaning changes were required.")

st.subheader("4. Data quality assessment")
quality, quality_details = assess_quality(cleaned)
q1,q2,q3,q4 = st.columns(4)
q1.metric("Overall quality score", f"{quality:.1f}/100")
q2.metric("Completeness", f"{quality_details['completeness']:.1f}%")
q3.metric("Uniqueness", f"{quality_details['uniqueness']:.1f}%")
q4.metric("Validity checks", f"{quality_details['validity']:.1f}%")
st.dataframe(quality_details["columns"], use_container_width=True)

st.subheader("5. Analytics dashboard")
analytics = build_analytics(cleaned)
for label, value in analytics["kpis"].items():
    st.metric(label, value)
render_visualisations(cleaned)

st.subheader("6. Decision support")
recommendations = generate_recommendations(cleaned, quality_details)
for item in recommendations:
    with st.container(border=True):
        st.markdown(f"**{item['priority']} · {item['title']}**")
        st.write(item["evidence"])
        st.write(f"**Suggested action:** {item['action']}")

st.subheader("7. Export")
excel_bytes = make_excel_report(raw, cleaned, audit, quality_details)
st.download_button("Download Excel report", excel_bytes, file_name="dataflow_intelligence_report.xlsx",
                   mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
txt = make_text_report(st.session_state["source_name"], raw, cleaned, audit, quality, recommendations)
st.download_button("Download ETL and insights report", txt, file_name="dataflow_report.txt", mime="text/plain")
st.download_button("Download cleaned CSV", cleaned.to_csv(index=False).encode("utf-8"),
                   file_name="cleaned_dataset.csv", mime="text/csv")
