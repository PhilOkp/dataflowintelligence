import streamlit as st
st.title("Data Quality Guide")
st.markdown("""
The current prototype reports:
- **Completeness:** proportion of cells containing values.
- **Uniqueness:** proportion of rows that are not exact duplicates.
- **Validity:** a preliminary numeric finite-value check.

These are starter indicators. Production use should add domain-specific rules, referential integrity, valid ranges, date constraints and business-key uniqueness.
""")
