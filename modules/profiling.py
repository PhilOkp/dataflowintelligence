import pandas as pd

def profile_dataset(df):
    rows=[]
    for col in df.columns:
        s=df[col]
        rows.append({
            "Column": str(col), "Data type": str(s.dtype), "Non-null": int(s.notna().sum()),
            "Missing": int(s.isna().sum()), "Missing %": round(s.isna().mean()*100,2),
            "Distinct values": int(s.nunique(dropna=True))
        })
    return pd.DataFrame(rows)
