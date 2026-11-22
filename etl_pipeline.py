import io
import os
import boto3
from dotenv import load_dotenv
import pandas as pd

# Load credentials from the .env file
load_dotenv()

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# Create the S3 client to talk to AWS
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION,
)


def upload_raw_excel(file_bytes, filename):
  """Uploads the original Excel file to the 'raw/' folder in S3."""
  raw_key = f"raw/{filename}"
  s3.put_object(Bucket=BUCKET_NAME, Key=raw_key, Body=file_bytes)
  print(f"Uploaded raw file to s3://{BUCKET_NAME}/{raw_key}")
  return raw_key


def run_etl(raw_key):
  """Reads the raw Excel file from S3, cleans every table, and saves JSON to 'processed/'."""
  # 1. EXTRACT: Download the Excel file from S3 into memory
  response = s3.get_object(Bucket=BUCKET_NAME, Key=raw_key)
  excel_bytes = response["Body"].read()

  # Read all sheets into a dictionary: { "SheetName": DataFrame }
  all_sheets = pd.read_excel(io.BytesIO(excel_bytes), sheet_name=None)
  processed_tables = []

  for sheet_name, df in all_sheets.items():
    print(f"Transforming table: {sheet_name}...")

    # 2. TRANSFORM:
    # a) Drop rows that are completely blank
    df.dropna(how="all", inplace=True)

    # b) Clean column names (e.g. "Customer ID" -> "customer_id")
    df.columns = [
        str(col).strip().lower().replace(" ", "_") for col in df.columns
    ]

    # c) Trim leading/trailing spaces from text columns
    for col in df.select_dtypes(include=["object"]).columns:
      df[col] = df[col].astype(str).str.strip()

    # d) Automatically clean ANY column containing ₹ or $ currency symbols
    for col in df.select_dtypes(include=["object"]).columns:
      if df[col].str.contains(r"^[₹$]", regex=True).any():
        df[col] = (
            df[col]
            .str.replace("₹", "", regex=False)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    # 3. LOAD: Save each cleaned table as JSON in S3 'processed/' folder
    clean_table_name = sheet_name.strip().lower().replace(" ", "_")
    processed_key = f"processed/{clean_table_name}.json"

    json_data = df.to_json(orient="records", indent=2)
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=processed_key,
        Body=json_data,
        ContentType="application/json",
    )
    print(f"Saved cleaned table to s3://{BUCKET_NAME}/{processed_key}")
    processed_tables.append(clean_table_name)

  return processed_tables


def fetch_processed_table(table_name):
  """Downloads a processed JSON table from S3 and returns it as a pandas DataFrame."""
  key = f"processed/{table_name}.json"
  response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
  json_content = response["Body"].read().decode("utf-8")
  return pd.read_json(io.StringIO(json_content))


def list_processed_tables():
  """Lists all processed JSON table names currently stored in S3."""
  response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix="processed/")
  tables = []
  for obj in response.get("Contents", []):
    key = obj["Key"]
    if key.endswith(".json"):
      table_name = key.replace("processed/", "").replace(".json", "")
      tables.append(table_name)
  return tables


# Quick test when running this file directly
if __name__ == "__main__":
  with open("sales_data.xlsx", "rb") as f:
    raw_s3_key = upload_raw_excel(f.read(), "sales_data.xlsx")
  tables = run_etl(raw_s3_key)
  print("ETL Complete! Processed tables:", tables)