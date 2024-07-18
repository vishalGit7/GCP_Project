
# (Optional) Define a service account for Cloud Build
resource "google_service_account" "build_sa" {
  account_id = "cloud-build-sa"
}