terraform {
  backend "gcs" {
    bucket = "linkedin_genai_bucket"
    prefix = "terraform/state"
  }
}

# Provider configuration (optional, if not using Application Default Credentials)
# provider "google" {
#   project     = "linkedin-genai"
#   credentials = file("credentials.json")  # Uncomment if using a service account key
# }
