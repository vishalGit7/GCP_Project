from google.cloud import storage

def process_file(bucket_name, filename):
  """Reads a CSV file from GCS and prints the content.

  Args:
    bucket_name: Name of the GCS bucket.
    filename: Name of the CSV file in the bucket.
  """
  # Access environment variables (replace with your own)
  bucket_name = os.environ.get('BUCKET_NAME')

  # Download the file from GCS
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(filename)
  data = blob.download_as_string()

  # Print the file content
  print(data.decode('utf-8'))  # Decode bytes to string

if __name__ == "__main__":
  # Replace with environment variables or command line arguments
  bucket_name = "your-bucket-name"
  filename = "your-file.csv"

  process_file(bucket_name, filename)
