import os
from flask import Flask, jsonify
from google.cloud import storage, bigquery

# Configure BigQuery client (replace with your project ID)
client = bigquery.Client(project='your-project-id')

app = Flask(__name__)


@app.route("/", methods=['POST'])
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

    try:
        # Download the file from GCS
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)

        blobs = bucket.list_blobs()
        for blob in blobs:
            # Process only the first file (assuming you want to handle one file per request)
            if blob.name.endswith('.csv'):
                data = blob.download_as_string().decode('utf-8')
                break

        # Load data into BigQuery (use error handling)

        table_ref = client.dataset(dataset_id).table(table_id)
        table = bigquery.Table(table_ref)


        errors = client.load_table_from_string(data, table, field_delimiter=';').result()  # Adjust delimiter if needed

        # Handle potential errors during loading
        if errors:
            error_string = ', '.join(err['errors'] for err in errors)
            return jsonify({'message': f"Failed to load data: {error_string}"}), 500

        return jsonify({'message': 'File processed and data loaded to BigQuery successfully!'})

    except Exception as e:
        return jsonify({'message': f"Error processing file: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)  # Run the Flask app for Cloud Run
