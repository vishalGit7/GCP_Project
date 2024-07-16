from google.cloud import storage
from google.cloud import bigquery
import os
import logging

logging.basicConfig(level=logging.INFO)

def process_file(filename, dataset_id, table_id):
  """Reads a CSV file from GCS and loads it to BigQuery table.

  Args:
    filename: Name of the CSV file in the bucket (retrieved from environment variable).
    dataset_id: ID of the BigQuery dataset (retrieved from environment variable).
    table_id: ID of the BigQuery table (retrieved from environment variable).
  """
  # Access environment variables
  bucket_name = os.environ.get('BUCKET_NAME')
  if not bucket_name:
    logging.error("Bucket name not found in environment variables.")
    return

  # Download the file from GCS
  try:
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(filename)
    data = blob.download_as_string()
  except Exception as e:
    logging.error(f"Error downloading file from GCS: {e}")
    return

  # Define BigQuery schema
  schema = [
      bigquery.SchemaField("username", "STRING", "REQUIRED"),
      # Add more fields as needed
  ]

  # Load data to BigQuery
  try:
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)

    load_job = bigquery_client.load_table_from_string(
        data,
        table_ref,
        job_config=bigquery.LoadJobConfig(
            schema=schema,
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            field_delimiter=",",
        ),
    )

    load_job.result()  # Wait for the load job to complete
    logging.info("Data loaded successfully!")
  except Exception as e:
    logging.error(f"Error loading data to BigQuery: {e}")
    return

if __name__ == "__main__":
  # Replace with environment variables
  filename = os.environ.get('FILENAME')  # Optional for on-demand execution
  dataset_id = os.environ.get('DATASET_ID')
  table_id = os.environ.get('TABLE_ID')

  if not all([filename, dataset_id, table_id]):
    logging.error("Missing required environment variables.")
    return

  process_file(filename, dataset_id, table_id)
