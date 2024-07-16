from google.cloud import storage
import pandas as pd

def main(request):
    """
    Cloud Run function to read CSV files from GCS and print contents.

    Args:
        request (flask.Request): The request object.
        <http://flask.pocoo.org/docs/1.0/api/#incoming-request-data>

    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <http://flask.pocoo.org/docs/1.0/api/#flask.make_response>.
    """

    # Get the CSV file name from the request (e.g., from a query parameter)
    file_name = request.args.get('file')

    # Check if a file name was provided
    if not file_name:
        return 'Please provide a CSV file name in the request (e.g., ?file=my_data.csv)'

    # GCS bucket name
    bucket_name = 'your-gcs-bucket-name'  # Replace with your bucket name

    # Create a Cloud Storage client
    storage_client = storage.Client()

    # Get the CSV file from GCS
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_name)

    # Download the CSV file to a string
    csv_data = blob.download_as_string().decode('utf-8')

    # Load the CSV data into a Pandas DataFrame
    df = pd.read_csv(io.StringIO(csv_data))

    # Print the DataFrame (or process it as needed)
    print(df)

    # Return a response
    return 'CSV file processed successfully!'
