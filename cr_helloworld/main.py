# Copyright 2020 Google, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START cloudbuild_python_flask]
import os

from flask import Flask
from google.cloud import storage

app = Flask(__name__)


@app.route("/")
def process_file(bucket_name, filename):
  print("start")
  """Reads a CSV file from GCS and prints the content.

  Args:
    bucket_name: Name of the GCS bucket.
    filename: Name of the CSV file in the bucket.
  """
  # Access environment variables (replace with your own)

  # Download the file from GCS
  client = storage.Client()
  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(filename)
  data = blob.download_as_string()

  # Print the file content
  print(data.decode('utf-8'))  # Decode bytes to string

if __name__ == "__main__":
  
  print("start within main")
  # Replace with environment variables or command line arguments
  process_file("winged-app-429513-b8_terraform", "username.csv")

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
# # [END cloudbuild_python_flask]