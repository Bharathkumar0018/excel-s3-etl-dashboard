# 📊 Excel to AWS S3 ETL Pipeline & Web Dashboard

An end-to-end data engineering and analytics project that ingests multi-sheet Excel workbooks containing database-style tables, runs an automated Python ETL pipeline, stores raw and cleaned JSON tables in **AWS S3**, and visualizes the processed data on an interactive **Streamlit** dashboard.

## Architecture
1. **Ingestion:** Upload any `.xlsx` workbook via the Streamlit web UI.
2. **Raw Storage (AWS S3):** Original workbooks are archived under the `raw/` prefix.
3. **ETL Processing (Python + Pandas):**
   - Extracts all sheets dynamically (`sheet_name=None`).
   - Drops completely empty rows and trims whitespace.
   - Standardizes column headers to `snake_case`.
   - Automatically detects and converts currency strings (`₹`, `$`) into numeric values.
4. **Processed Storage (AWS S3):** Outputs clean, structured JSON tables under the `processed/` prefix.
5. **Analytics Dashboard (Streamlit):** Dynamically discovers tables in S3, displays KPIs, generates interactive bar charts, and provides searchable data tables.

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/excel-s3-etl-dashboard.git](https://github.com/YOUR_USERNAME/excel-s3-etl-dashboard.git)
   cd excel-s3-etl-dashboard