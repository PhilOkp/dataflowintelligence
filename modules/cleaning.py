import pandas as pd
import numpy as np

def clean_dataset(df, remove_duplicates=True, trim_text=True, standardise_text=True,
                  drop_empty_cols=True, infer_types=True, missing_strategy="Keep as missing"):
    """Return a cleaned copy and a human-readable audit log."""
    result = df.copy(deep=True)
    audit = []

    def record(operation, column, affected, explanation):
        audit.append({"Operation": operation, "Column": column, "Affected": int(affected),
                      "Explanation": explanation})

    if remove_duplicates:
        n = int(result.duplicated().sum())
        if n:
            result = result.drop_duplicates().copy()
        record("Remove duplicates", "All columns", n, "Removed fully duplicated records.")

    if trim_text or standardise_text:
        for col in result.select_dtypes(include=["object","string"]).columns:
            before = result[col].copy()
            s = result[col].astype("string")
            if trim_text:
                s = s.str.strip()
            if standardise_text:
                s = s.str.replace(r"\s+", " ", regex=True)
            changed = int((before.fillna("__NA__").astype(str) != s.fillna("__NA__").astype(str)).sum())
            result[col] = s
            if changed:
                record("Text standardisation", col, changed,
                       "Trimmed leading/trailing spaces and/or collapsed repeated whitespace.")

    if drop_empty_cols:
        empty_cols = [c for c in result.columns if result[c].isna().all()]
        if empty_cols:
            result = result.drop(columns=empty_cols)
            record("Remove empty columns", ", ".join(map(str, empty_cols)), len(empty_cols),
                   "Removed columns containing no observed values.")

    if infer_types:
        for col in result.columns:
            if result[col].dtype == "object":
                non_null = result[col].dropna()
                if len(non_null) == 0:
                    continue
                numeric = pd.to_numeric(result[col], errors="coerce")
                if numeric.notna().sum() / max(result[col].notna().sum(),1) >= 0.85:
                    result[col] = numeric
                    record("Type conversion", col, int(numeric.notna().sum()),
                           "Converted values that were predominantly numeric.")
                    continue
                dates = pd.to_datetime(result[col], errors="coerce")
                if dates.notna().sum() / max(result[col].notna().sum(),1) >= 0.85:
                    result[col] = dates
                    record("Type conversion", col, int(dates.notna().sum()),
                           "Converted values that were predominantly dates.")

    before_missing = int(result.isna().sum().sum())
    if missing_strategy == "Drop rows with missing values":
        old = len(result)
        result = result.dropna().copy()
        record("Missing values", "All columns", old-len(result), "Dropped rows containing at least one missing value.")
    elif missing_strategy in ("Fill numeric with median","Fill numeric with mean"):
        for col in result.select_dtypes(include=np.number).columns:
            n = int(result[col].isna().sum())
            if n:
                value = result[col].median() if missing_strategy.endswith("median") else result[col].mean()
                result[col] = result[col].fillna(value)
                record("Missing-value imputation", col, n, f"Filled missing values using {missing_strategy.split()[-1]}.")
    elif missing_strategy == "Fill with mode":
        for col in result.columns:
            n = int(result[col].isna().sum())
            modes = result[col].mode(dropna=True)
            if n and not modes.empty:
                result[col] = result[col].fillna(modes.iloc[0])
                record("Missing-value imputation", col, n, "Filled missing values using the most frequent value.")
    return result, audit
