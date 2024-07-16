import re
from google.cloud import storage
from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def hello_gcs(event, context):
    bq_client = bigquery.Client()
    bucket = storage.Client().bucket("your-bucket-name")

    for blob in bucket.list_blobs(prefix="your-folder-name/"):
        if ".csv" in blob.name:
            # Extract the file name for the BigQuery table ID
            csv_filename = re.findall(r".*/(.*).csv", blob.name)
            bq_table_id = "your-project.dataset-name." + csv_filename[0]

            try:
                # Check if the table already exists and skip uploading it
                bq_client.get_table(bq_table_id)
                print(f"Table {bq_table_id} already exists. Not uploaded.")
            except NotFound:
                # If the table is not found, upload it
                uri = f"gs://your-bucket-name/{blob.name}"
                job_config = bigquery.LoadJobConfig(
                    autodetect=True,
                    skip_leading_rows=1,
                    source_format=bigquery.SourceFormat.CSV,
                )
                load_job = bq_client.load_table_from_uri(uri, bq_table_id, job_config=job_config)
                load_job.result()  # Wait for the job to complete
                print(f"Uploaded file: {blob.name} to table: {bq_table_id}")

# This function is triggered by Pub/Sub whenever there is a new file in the GCS bucket
