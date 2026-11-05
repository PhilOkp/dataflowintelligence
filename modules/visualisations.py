import streamlit as st
import pandas as pd
import plotly.express as px

def render_visualisations(df):
    numeric=list(df.select_dtypes(include="number").columns)
    categorical=[c for c in df.columns if df[c].nunique(dropna=True)<=30 and c not in numeric]
    date_cols=[c for c in df.columns if pd.api.types.is_datetime64_any_dtype(df[c])]
    charts=[]
    if numeric:
        col=numeric[0]
        fig=px.histogram(df,x=col,title=f"Distribution of {col}",nbins=30)
        charts.append(("Distribution",fig))
    if len(numeric)>=2:
        fig=px.scatter(df,x=numeric[0],y=numeric[1],title=f"{numeric[0]} vs {numeric[1]}")
        charts.append(("Relationship",fig))
    if categorical and numeric:
        grouped=df.groupby(categorical[0],dropna=False)[numeric[0]].mean().reset_index().head(20)
        fig=px.bar(grouped,x=categorical[0],y=numeric[0],title=f"Average {numeric[0]} by {categorical[0]}")
        charts.append(("Category comparison",fig))
    if date_cols and numeric:
        temp=df[[date_cols[0],numeric[0]]].dropna().copy()
        if not temp.empty:
            temp=temp.set_index(date_cols[0]).resample("ME")[numeric[0]].sum().reset_index()
            fig=px.line(temp,x=date_cols[0],y=numeric[0],title=f"{numeric[0]} over time")
            charts.append(("Time trend",fig))
    if len(numeric)>=1:
        corr=df[numeric].corr(numeric_only=True)
        if corr.shape[0]>=2:
            fig=px.imshow(corr,text_auto=".2f",title="Numeric correlation matrix",aspect="auto")
            charts.append(("Correlation",fig))
    if not charts:
        st.info("Not enough numeric, categorical or date fields were detected to create meaningful charts.")
    for i in range(0,len(charts),2):
        cols=st.columns(2)
        for j,(name,fig) in enumerate(charts[i:i+2]):
            with cols[j]:
                st.plotly_chart(fig,use_container_width=True)
