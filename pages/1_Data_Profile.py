import streamlit as st
import pandas as pd
from modules.profiling import profile_dataset
st.title("Data Profile")
st.write("This page is a companion page for future multi-page workflows. Upload and profile datasets from the main DataFlow Intelligence page.")
st.info("The main app currently manages the active dataset and its processing session.")
