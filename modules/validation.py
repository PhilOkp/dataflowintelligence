import pandas as pd
import numpy as np

def assess_quality(df):
    total_cells = max(df.shape[0]*df.shape[1],1)
    completeness = 100*(1-df.isna().sum().sum()/total_cells)
    uniqueness = 100*(1-df.duplicated().mean()) if len(df) else 100.0
    checks=[]
    validity_scores=[]
    for col in df.columns:
        s=df[col]
        nonnull=s.dropna()
        if pd.api.types.is_numeric_dtype(s):
            valid = nonnull.map(lambda x: np.isfinite(x) if isinstance(x,(int,float,np.number)) else True).mean() if len(nonnull) else 100
            valid = float(valid*100 if valid <= 1 else valid)
        else:
            valid=100.0
        validity_scores.append(valid)
        checks.append({"Column":str(col),"Missing":int(s.isna().sum()),
                       "Missing %":round(s.isna().mean()*100,2),
                       "Distinct":int(s.nunique(dropna=True)),
                       "Duplicate values":int(s.duplicated().sum()),
                       "Type":str(s.dtype),"Validity %":round(valid,2)})
    validity=float(np.mean(validity_scores)) if validity_scores else 100.0
    score=float(np.mean([completeness,uniqueness,validity]))
    return score, {"completeness":float(completeness),"uniqueness":float(uniqueness),
                   "validity":validity,"columns":pd.DataFrame(checks)}
