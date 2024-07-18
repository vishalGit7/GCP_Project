variable "project_id" {
  type = string
  default = "winged-app-429513-b8"
  description = "Google cloud project id"
}

# (Optional) Define a service account for Cloud Build
resource "google_service_account" "build_sa" {
  account_id = "cloud-build-sa"
  project = var.project_id
}

resource "google_service_account_iam_member" "storage_access" {
  role = "roles/storage.admin"  # Replace with the desired role
  member = "serviceAccount:{{ google_service_account.build_sa.email }}"
  project = var.project_id
}