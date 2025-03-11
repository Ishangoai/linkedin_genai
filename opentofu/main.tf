# Variable definitions for sensitive data
variable "gemini_api_key" {
  description = "API key for Gemini"
  type        = string
  sensitive   = true
}

variable "slack_api_token" {
  description = "API token for Slack"
  type        = string
  sensitive   = true
}

variable "billing_account" {
  description = "Billing account ID"
  type        = string
}

variable "org_id" {
  description = "Organization ID"
  type        = string
}

terraform {
  backend "gcs" {
    bucket = "linkedin_genai_bucket"
    prefix = "terraform/state"
  }
}

# Provider configuration (optional, if not using Application Default Credentials)
# provider "google" {
#   project     = "linkedin-genai"
#   # credentials = file("credentials.json")  # Uncomment if using a service account key
# }

resource "google_artifact_registry_repository" "linkedin_genai_gcr" {
  cleanup_policy_dry_run = true
  format                 = "DOCKER"
  location               = "europe-west2"
  mode                   = "STANDARD_REPOSITORY"
  project                = "linkedin-genai"
  repository_id          = "linkedin-genai-gcr"
}
# terraform import google_artifact_registry_repository.linkedin_genai_gcr projects/linkedin-genai/locations/europe-west2/repositories/linkedin-genai-gcr

resource "google_project" "linkedin_genai" {
  auto_create_network = true
  billing_account     = var.billing_account
  name                = "Linkedin GenAI"
  org_id              = var.org_id
  project_id          = "linkedin-genai"
}
# terraform import google_project.linkedin_genai projects/linkedin-genai

resource "google_service_account" "linkedin_genai_service" {
  account_id   = "linkedin-genai-service"
  display_name = "linkedin-genai-service"
  project      = "linkedin-genai"
}
# terraform import google_service_account.linkedin_genai_service projects/linkedin-genai/serviceAccounts/linkedin-genai-service@linkedin-genai.iam.gserviceaccount.com

resource "google_cloud_run_v2_service" "linkedin_genai_service" {
  client         = "gcloud"
  client_version = "511.0.0"
  ingress        = "INGRESS_TRAFFIC_ALL"
  launch_stage   = "GA"
  location       = "europe-west2"
  name           = "linkedin-genai-service"
  project        = "linkedin-genai"
  template {
    containers {
      env {
        name  = "GEMINI_API_KEY"
        value = var.gemini_api_key
      }
      env {
        name  = "SLACK_API_TOKEN"
        value = var.slack_api_token
      }
      image = "europe-west2-docker.pkg.dev/linkedin-genai/linkedin-genai-gcr/linkedin-genai-image:7dc035f1e064c22eb6e9fa34ef5b12463cfadf15"
      name  = "linkedin-genai-image-1"
      ports {
        container_port = 8080
        name           = "http1"
      }
      resources {
        cpu_idle = true
        limits = {
          cpu    = "1000m"
          memory = "512Mi"
        }
        startup_cpu_boost = true
      }
      startup_probe {
        failure_threshold     = 1
        initial_delay_seconds = 0
        period_seconds        = 240
        tcp_socket {
          port = 8080
        }
        timeout_seconds = 240
      }
    }
    max_instance_request_concurrency = 80
    scaling {
      max_instance_count = 10
    }
    service_account = "linkedin-genai-service@linkedin-genai.iam.gserviceaccount.com"
    timeout         = "300s"
  }
  traffic {
    percent = 100
    type    = "TRAFFIC_TARGET_ALLOCATION_TYPE_LATEST"
  }
}
# terraform import google_cloud_run_v2_service.linkedin_genai_service projects/linkedin-genai/locations/europe-west2/services/linkedin-genai-service

resource "google_storage_bucket" "linkedin_genai_bucket" {
  force_destroy               = false
  location                    = "EUROPE-WEST2"
  name                        = "linkedin_genai_bucket"
  project                     = "linkedin-genai"
  public_access_prevention    = "enforced"
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
}
# terraform import google_storage_bucket.linkedin_genai_bucket linkedin_genai_bucket
