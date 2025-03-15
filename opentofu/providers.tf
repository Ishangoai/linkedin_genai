
terraform {
  backend "gcs" {
    bucket  = "linkedin_genai_bucket"
    prefix  = "tofu/state"
  }
}