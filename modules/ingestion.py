import io
import pandas as pd

def load_dataset(file_bytes: bytes, filename: str, sheet_name=0) -> pd.DataFrame:
    """Load CSV or Excel bytes into a DataFrame."""
    name = filename.lower()
    stream = io.BytesIO(file_bytes)
    if name.endswith(".csv"):
        try:
            return pd.read_csv(stream)
        except UnicodeDecodeError:
            stream.seek(0)
            return pd.read_csv(stream, encoding="latin-1")
    if name.endswith((".xlsx", ".xls")):
        return pd.read_excel(stream, sheet_name=sheet_name)
    raise ValueError("Unsupported file type. Please upload CSV or Excel.")
