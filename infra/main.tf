variable "project_id" {
  type = string
  default = "winged-app-429513-b8"
  description = "Google cloud project id"
}

# (Optional) Define a service account for Cloud Build
resource "google_service_account" "build_sa" {
  account_id = "cloud-build-cr"
  project = var.project_id
}

resource "google_service_account_iam_member" "admin-account-iam" {
  service_account_id = google_service_account.build_sa.name
  role               = "roles/storage.objectCreator"
  member            = "serviceAccount:${google_service_account.build_sa.email}"

depends_on = [ google_service_account.build_sa ]
}