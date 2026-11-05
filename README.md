# DataFlow Intelligence – Modular Streamlit Prototype

Created by **Philip Okposo | Naijadataman**.

DataFlow Intelligence helps clean, validate, and analyze datasets for clearer insights.

## 1. Requirements
- Python 3.10 or newer
- Internet connection for installing packages

## 2. Install and run
Open a terminal in this project folder:

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Using `python -m streamlit` runs Streamlit from the same Python environment and
works even when the `streamlit` command is not on `PATH`.

## 3. Included functionality
- CSV and Excel ingestion
- Initial dataset profiling
- Configurable cleaning and an ETL audit log
- Basic data quality indicators
- Adaptive Plotly charts
- Rule-based recommendations
- CSV, Excel and text report downloads

## 4. Important limitations
This is a development prototype, not yet a production-grade enterprise platform. The validity score is deliberately preliminary; there are no user accounts, database connectors, role permissions, server-side processing queue, automated test suite or deployment configuration. Review transformations and recommendations before operational use. Always protect confidential or personally identifiable data.

## 5. Deployment
Push this folder to a GitHub repository. In Streamlit Community Cloud, create an app, select the repository and branch, and set `app.py` as the main file. Add any secrets through the platform's secrets manager; never commit credentials.

## 6. Suggested next development steps
1. Add unit tests for each cleaning and validation rule.
2. Add configurable business rules and Pandera schemas.
3. Add robust Excel sheet selection and multi-file ingestion.
4. Add database connectors with secure credentials.
5. Add authentication, audit history, logging and deployment monitoring.
6. Add domain-aware insight generation and report templates.
