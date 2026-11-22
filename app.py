from etl_pipeline import fetch_processed_table, list_processed_tables, run_etl, upload_raw_excel
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Universal Excel ETL Dashboard", layout="wide")
st.title("📊 Universal Excel to AWS S3 ETL Dashboard")
st.markdown(
    "Upload **any** Excel workbook with database-style tables. The pipeline"
    " cleans every sheet, stores it in AWS S3, and dynamically builds charts"
    " and tables."
)

# 1. Sidebar: Upload & Run ETL
with st.sidebar:
  st.header("1. Upload & Run ETL")
  uploaded_file = st.file_uploader("Upload Any Excel File (.xlsx)", type=["xlsx"])

  if uploaded_file is not None:
    if st.button("🚀 Upload to S3 & Run ETL", type="primary"):
      with st.spinner("Processing all sheets and saving to S3..."):
        raw_key = upload_raw_excel(uploaded_file.getvalue(), uploaded_file.name)
        tables = run_etl(raw_key)
        st.success(f"Done! Processed {len(tables)} table(s).")

# 2. Discover whatever tables currently exist in S3
available_tables = list_processed_tables()

if not available_tables:
  st.info(
      "No processed tables in S3 yet. Upload any `.xlsx` file in the left"
      " sidebar to begin!"
  )
else:
  st.header("2. Select a Table to Explore")
  selected_table = st.selectbox(
      "Choose a processed table from AWS S3:", available_tables
  )

  # Load the chosen table from S3
  df = fetch_processed_table(selected_table)

  # Automatically detect numeric vs. text columns
  numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
  text_cols = df.select_dtypes(exclude=["number"]).columns.tolist()

  # Top KPI Metrics Row
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Rows", len(df))
  col2.metric("Total Columns", len(df.columns))

  if numeric_cols:
    default_num = numeric_cols[0]
    col3.metric(f"Total ({default_num})", f"{df[default_num].sum():,.2f}")
  else:
    col3.metric("Numeric Columns", 0)

  st.divider()

  # Dynamic Chart Builder (works with ANY column names)
  if text_cols and numeric_cols:
    st.subheader("3. Dynamic Chart")
    c1, c2 = st.columns(2)
    with c1:
      x_col = st.selectbox("Group by (Category Column):", text_cols)
    with c2:
      y_col = st.selectbox("Measure (Numeric Column):", numeric_cols)

    grouped_df = df.groupby(x_col, as_index=False)[y_col].sum()
    st.bar_chart(grouped_df, x=x_col, y=y_col)
    st.divider()

  # Full Searchable Data Table
  st.subheader(f"4. Cleaned Data: `{selected_table}`")
  st.dataframe(df, width="stretch")  #