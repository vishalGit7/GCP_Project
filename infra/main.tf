variable "project_id" {
  type = string
  default = "winged-app-429513-b8"
  description = "Google cloud project id"
}

resource "google_storage_bucket" "gcs-landing-bucket" {
  name          = "fileladingbucket_${var.project_id}"
  location      = "us-central1"
  force_destroy = true

  uniform_bucket_level_access = true

}

resource "google_storage_bucket_object" "empty_folder" {
  name   = "landing_data /" # folder for landing_files
  content = " "
  bucket = google_storage_bucket.gcs-landing-bucket.name
  depends_on = [ google_storage_bucket.gcs-landing-bucket ]
}

resource "google_service_account" "build_sa" {
  account_id = "cloud-build-cr"
  project = var.project_id
}

resource "google_project_iam_binding" "service_account_role" {
   project = var.project_id
  for_each = toset([
        "roles/storage.admin",
        "roles/logging.logWriter",
        "roles/artifactregistry.repositories.uploadArtifacts",
        "roles/run.deployer"

  ])
  role    = each.key

  members  = ["serviceAccount:${google_service_account.build_sa.email}"]
  depends_on = [ google_service_account.build_sa]
}

resource "google_bigquery_dataset" "dataset" {
  dataset_id                  = "landing_dataset"
  friendly_name               = "landing_dataset"
  description                 = "This is a dataset which contains landing tables"
  location                    = "us-central1"
  default_table_expiration_ms = 3600000

   labels = {
    env = "dev"
  }

}

resource "google_bigquery_table" "landing_table" {
  dataset_id = google_bigquery_dataset.dataset.dataset_id
  table_id   = "landing_table"

  time_partitioning {
    type = "DAY"
  }

  labels = {
    env = "default"
  }

  schema = <<EOF

[
  {
    "name": "product_sku",
    "mode": "REQUIRED",
    "type": "STRING",
    "description": "product sku value"
  },
  {
    "name": "transaction_time",
    "mode": "NULLABLE",
    "type": "TIMESTAMP"
  },
  {
    "name": "transaction_volume",
    "mode": "NULLABLE",
    "type": "INTEGER"
  },
  {
    "name": "transaction_venue",
    "mode": "NULLABLE",
    "type": "STRING"
  }
]
EOF

depends_on = [ google_bigquery_dataset.dataset ]

}

resource "google_cloudbuild_trigger" "github_trigger" {
  name = "my-cloudbuild-trigger"
  location = "us-central1"  # Adjust region if needed
  filename = "./infra/cloudbuild.yaml"
  # Configure GitHub source
  github {
    owner = "vishalGit7"  # Your GitHub username
    name  = "GCP_Project"      # Replace with your actual repository name
    
    push {
      branch = "^cr_nihilient$"  # Trigger on pushes to this branch (replace)
    }
  }
  service_account = google_service_account.build_sa.id
  depends_on = [ google_service_account_iam_binding.service_account_role ]

  # Optional: Specify build configuration file (replace with your path)
  

  # Optional: Ignore specific files during build
  # ignored_files = [".gitignore"]
}