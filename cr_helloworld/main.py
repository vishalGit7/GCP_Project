from google.cloud import storage
from google.cloud import bigquery

import os

def process_file(filename, dataset_id, table_id):
  """Reads a CSV file from GCS and loads it to BigQuery table.

  Args:
    filename: Name of the CSV file in the bucket (retrieved from environment variable).
    dataset_id: ID of the BigQuery dataset (retrieved from environment variable).
    table_id: ID of the BigQuery table (retrieved from environment variable).
  """
  # Access environment variables
  bucket_name = os.environ.get('winged-app-429513-b8_terraform')

  # Download the file from GCS
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(filename)
  data = blob.download_as_string()

  # Load data to BigQuery
  bigquery_client = bigquery.Client()
  dataset_ref = bigquery_client.dataset(dataset_id)
  table_ref = dataset_ref.table(table_id)

  load_job = bigquery_client.load_table_from_string(
      data,
      table_ref,
      field_delimiter=",",  # Change this if your delimiter is different
      skip_leading_rows=1  # Skip header row (optional)
  )

  load_job.result()  # Wait for the load job to complete

if __name__ == "__main__":
  # Replace with environment variables
  filename = os.environ.get('username.csv')  # Optional for on-demand execution
  dataset_id = os.environ.get('winged-app-429513-b8.stage_dataset')
  table_id = os.environ.get('winged-app-429513-b8.stage_dataset.usernames')

  process_file(filename, dataset_id, table_id)

  print("Data loaded successfully!")
