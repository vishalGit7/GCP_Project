terraform {
  backend "gcs" {
    bucket  = "winged-app-429513-b8_terraform"
    prefix  = "cr_gcs_to_bq/state"
  }
}