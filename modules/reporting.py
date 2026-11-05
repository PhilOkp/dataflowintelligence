from io import BytesIO
import pandas as pd

def make_excel_report(raw, cleaned, audit, quality):
    output=BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        raw.to_excel(writer,index=False,sheet_name="Source data")
        cleaned.to_excel(writer,index=False,sheet_name="Cleaned data")
        pd.DataFrame(audit or [{"Operation":"No changes","Column":"","Affected":0,"Explanation":"No cleaning changes recorded."}]).to_excel(writer,index=False,sheet_name="ETL audit")
        quality["columns"].to_excel(writer,index=False,sheet_name="Quality details")
        pd.DataFrame([{"Metric":"Completeness","Score":quality["completeness"]},
                      {"Metric":"Uniqueness","Score":quality["uniqueness"]},
                      {"Metric":"Validity","Score":quality["validity"]}]).to_excel(writer,index=False,sheet_name="Quality summary")
    return output.getvalue()

def make_text_report(filename, raw, cleaned, audit, score, recommendations):
    lines=["DATAFLOW INTELLIGENCE - ETL REPORT",f"Source file: {filename}",
           f"Source shape: {raw.shape[0]} rows x {raw.shape[1]} columns",
           f"Processed shape: {cleaned.shape[0]} rows x {cleaned.shape[1]} columns",
           f"Overall data quality score: {score:.1f}/100","","ETL OPERATIONS"]
    lines += [f"- {x['Operation']} | {x['Column']} | affected: {x['Affected']} | {x['Explanation']}" for x in audit] or ["- No changes recorded."]
    lines += ["","RECOMMENDATIONS"]
    lines += [f"- {x['priority']}: {x['title']}. Evidence: {x['evidence']} Action: {x['action']}" for x in recommendations]
    lines += ["","Note: Recommendations are rule-based prompts for review, not proof of causation or substitutes for domain expertise."]
    return "\n".join(lines)
