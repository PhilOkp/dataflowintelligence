import pandas as pd

def build_analytics(df):
    numeric=df.select_dtypes(include="number")
    kpis={
        "Records analysed": f"{len(df):,}",
        "Fields analysed": f"{len(df.columns):,}",
        "Numeric fields": f"{len(numeric.columns):,}",
        "Missing values": f"{int(df.isna().sum().sum()):,}"
    }
    return {"kpis":kpis, "numeric_summary":numeric.describe().T if len(numeric.columns) else pd.DataFrame()}
