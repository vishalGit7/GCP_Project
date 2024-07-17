import os
from flask import Flask, jsonify
from google.cloud import storage, bigquery

# Configure BigQuery client (replace with your project ID)
# client = bigquery.Client(project='your-project-id')

app = Flask(__name__)


@app.route("/", methods=['POST','GET'])
def process_file():
    """Reads a CSV file from GCS, loads it into BigQuery, and returns a success message.

    Environment variables:
        BUCKET_NAME: Name of the GCS bucket.
        DATASET_ID: ID of the BigQuery dataset to write to.
        TABLE_ID: ID of the BigQuery table to create or append to.
        SCHEMA (optional): Schema definition for the BigQuery table (JSON format).
    """

    # Access environment variables
    bucket_name = os.environ.get('BUCKET_NAME')
    dataset_id = os.environ.get('DATASET_ID')
    table_id = os.environ.get('TABLE_ID')
    landing_folder_prefix = os.environ.get('LANDING_DATA_PATH')
   

    try:
        # Download the file from GCS
        gcs_client = storage.Client()
        bucket = gcs_client.get_bucket(bucket_name)
        bq_client = bigquery.Client(project='winged-app-429513-b8')
        blobs = bucket.list_blobs(prefix = landing_folder_prefix )
        # blobs = bucket.list_blobs(prefix = "winged-app-429513-b8_terraform/landing_data")
        for blob in blobs:
            # print(f"The filename is {str(blob.name)}")
            # Process only the first file (assuming you want to handle one file per request)
            if blob.name.endswith('.csv'):
                print(f"The filename is {str(blob.name)}")
                try:
                    print(f"The filename is {str(blob.name)}")
                    data = blob.download_as_string().decode('utf-8')
                    print(data)
                    uri = f"gs://{bucket.name}/{blob.name}"              

        # Load data into BigQuery (use error handling)
                    job_config = bigquery.LoadJobConfig(
                        source_format = "CSV",
                        field_delimiter = ";",
                        skip_leading_rows = 1,
                        write_disposition = "WRITE_APPEND",
                        schema = [
                            {"name": "Username", "type": "STRING"},
                            {"name":"Identifier" , "type": "STRING"},
                            {"name": "First_name", "type": "STRING"},
                            {"name": "Last_name", "type": "STRING"},
                            
                        ]
                        
                    )
                    load_job = bq_client.load_table_from_uri(uri, table_id, job_config =job_config)  # Make an API request.
                    load_job.result()
                    return jsonify({'message': 'File processed and data loaded to BigQuery successfully!'})
    
                except Exception as e:
                    print(f"Error processing file {blob.name}: {str(e)}")

        
    except Exception as e:
        return jsonify({'message': f"Error processing file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug = True)  # Run the Flask app for Cloud Run
