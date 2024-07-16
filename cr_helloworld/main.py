import os
from flask import Flask, request
from google.cloud import storage
app = Flask(__name__)

@app.route("/", methods=["POST"])
def process_file():  
        bucket_name = "winged-app-429513-b8_terraform"
        print("Start")
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)

        blob_list = list(bucket.list_blobs(prefix= prefix))
        for blob in blob_list[1:]:
            print(blob)
            file_content = blob.download_as_text()

        # Print the file content
        print(f"File content for {blob}:\n{file_content}")

        return "File content printed successfully!"

# Deploy this Cloud Run service to handle HTTP requests
