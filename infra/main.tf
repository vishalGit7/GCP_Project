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

resource "google_service_account" "build_sa" {
  account_id = "cloud-build-cr"
  project = var.project_id
}

resource "google_service_account_iam_binding" "sa-role" {
  service_account_id = google_service_account.build_sa.name
  role = "roles/iam.serviceAccountUser"
  members = ["serviceAccount: ${ google_service_account.build_sa.email }"]
  depends_on = [ google_service_account.build_sa,google_storage_bucket.gcs-landing-bucket ]
}

