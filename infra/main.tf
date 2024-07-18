variable "project_id" {
  type = string
  description = "The Google Cloud project ID"
}

# (Optional) Define a service account for Cloud Build
resource "google_service_account" "build_sa" {
  account_id = "cloud-build-sa"
  project = var.project_id
}