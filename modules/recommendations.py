def generate_recommendations(df, quality):
    items=[]
    missing=int(df.isna().sum().sum())
    if missing:
        items.append({"priority":"High","title":"Investigate missing data",
            "evidence":f"The processed dataset still contains {missing:,} missing cells.",
            "action":"Identify why these values are absent. Decide whether to collect, retain, impute or exclude them based on business meaning."})
    duplicates=int(df.duplicated().sum())
    if duplicates:
        items.append({"priority":"Medium","title":"Review duplicate records",
            "evidence":f"{duplicates:,} fully duplicated rows remain.",
            "action":"Confirm whether repeated rows are valid transactions or accidental duplicates before removing them."})
    if quality["completeness"] < 95:
        items.append({"priority":"High","title":"Improve data completeness",
            "evidence":f"Completeness is {quality['completeness']:.1f}%.",
            "action":"Prioritise important fields and strengthen data capture rules at the point of entry."})
    if quality["uniqueness"] < 98:
        items.append({"priority":"Medium","title":"Check record uniqueness",
            "evidence":f"Row-level uniqueness score is {quality['uniqueness']:.1f}%.",
            "action":"Define a business key, such as transaction ID or customer ID, and investigate repeated records."})
    if len(df.select_dtypes(include="number").columns)==0:
        items.append({"priority":"Medium","title":"Review field types",
            "evidence":"No numeric fields were detected.",
            "action":"Check whether quantities, amounts or measurements are stored as text and convert only after confirming their meaning."})
    if not items:
        items.append({"priority":"Low","title":"Continue routine data monitoring",
            "evidence":"The basic automated checks did not identify a major issue.",
            "action":"Validate the dataset against business rules and monitor quality over time. A high score does not guarantee business correctness."})
    return items
