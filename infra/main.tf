# Configure GCP Provider
provider "google" {
  project = "winged-app-429513-b8"
  region  = "asia-south1"
}

# Service Account
resource "google_service_account" "build_sa" {
  account_id = "build-sa"  # Choose the same name as in step 1
}

# Cloud Build Trigger
resource "google_cloudbuild_trigger" "manual-trigger" {
  name        = "manual-trigger"
  service_account = google_service_account.build_sa.id

  source_to_build {
    uri       = "https://github.com/vishalGit7/GCP_Project"
    ref       = "refs/heads/learning_cloudrun"
    repo_type = "GITHUB"
  }

  git_file_source {
    path      = "infra/cloudbuild.yaml"
    uri       = "https://github.com/vishalGit7/GCP_Project"
    revision  = "refs/heads/learning_cloudrun"
    repo_type = "GITHUB"
  }
}

# Cloud Run Service
resource "google_cloudrun_service_v2" "your_service" {
  name        = "cr-tf"
  location    = google_cloud_region.region.name  # Reference region from provider
  template {
    spec {
      container {
        image = "gcr.io/$PROJECT_ID/cr-tf:$COMMIT_SHA"
      }
    }
  }

  # Optional: Additional configuration for scaling, environment variables, etc.
}

# Reference region from provider
resource "google_cloud_region" "region" {
  name = var.region
}