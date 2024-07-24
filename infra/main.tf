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
  name   = "landing_data/" # folder for landing_files
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
        "roles/logging.logWriter"
        
  ])
  role    = each.key

  members  = ["serviceAccount:${google_service_account.build_sa.email}"]
  depends_on = [ google_service_account.build_sa]
}
resource "google_project_iam_member" "cloud_run_role" {
  project = var.project_id
  role = "roles/run.admin"

  member = "serviceAccount:${google_service_account.build_sa.email}"
  depends_on = [google_service_account.build_sa]
}
resource "google_project_iam_member" "artifactrole" {
  project = var.project_id
  role = "roles/artifactregistry.admin"  # Example role for basic deployment
  member = "serviceAccount:${google_service_account.build_sa.email}"
  depends_on = [google_service_account.build_sa]
}
resource "google_project_iam_member" "eventrole" {
  project = var.project_id
  role = "roles/eventarc.developer"  
  member = "serviceAccount:${google_service_account.build_sa.email}"
  depends_on = [google_service_account.build_sa]
}

resource "google_project_iam_member" "bqrole" {
  project = var.project_id
  role = "roles/bigquery.jobUser"  
  member = "serviceAccount:${google_service_account.build_sa.email}"
  depends_on = [google_service_account.build_sa]
}
resource "google_project_iam_member" "iamrole" {
  project = var.project_id
  role = "roles/iam.serviceAccountUser"  
  member = "serviceAccount:${google_service_account.build_sa.email}"
  depends_on = [google_service_account.build_sa]
}

# data "google_compute_default_service_account" "default" {
# }
# resource "google_service_account_iam_member" "impersonation_role" {
#   service_account_id = google_service_account.build_sa.name
#   role = 
#   member = "serviceAccount:${data.google_compute_default_service_account.default}"
#   depends_on = [google_service_account.build_sa]
# }

resource "google_bigquery_dataset" "stg_dataset" {
  dataset_id                  = "stg_dataset"
  friendly_name               = "landing_dataset"
  description                 = "This is a dataset which contains landing tables"
  location                    = "us-central1"
  default_table_expiration_ms = 3600000
 
   labels = {
    env = "dev"
  }

}

resource "google_bigquery_table" "stg_table" {
  dataset_id = google_bigquery_dataset.stg_dataset.dataset_id
  table_id   = "landing_table"
  deletion_protection = false

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

depends_on = [ google_bigquery_dataset.stg_dataset ]

}


resource "google_cloudbuild_trigger" "github_trigger" {
  name = "my-cloudbuild-trigger"
  location = "us-central1"  # Adjust region if needed
  filename = "infra/cloudbuild.yaml"
  # Configure GitHub source
  github {
    owner = "vishalGit7"  # Your GitHub username
    name  = "GCP_Project"      # Replace with your actual repository name
    
    push {
      branch = "^cr_nihilient$"  # Trigger on pushes to this branch (replace)
    }
  }
  service_account = google_service_account.build_sa.id
  depends_on = [ google_project_iam_binding.service_account_role,google_bigquery_dataset.stg_dataset,google_bigquery_table.stg_table,
               google_storage_bucket.gcs-landing-bucket,
                 google_storage_bucket_object.empty_folder,google_project_iam_binding.service_account_role,
                 google_project_iam_member.artifactrole,google_project_iam_member.cloud_run_role,
                 google_service_account.build_sa ]

}

output "cloudbuild_trigger_name" {
  value = google_cloudbuild_trigger.github_trigger.name
}