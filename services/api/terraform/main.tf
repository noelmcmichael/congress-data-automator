# Terraform configuration for Congressional Data API Service
# Supports Google Cloud Platform deployment

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 5.0"
    }
  }
}

# Configure the Google Cloud Provider
provider "google" {
  project = var.project_id
  region  = var.region
}

provider "google-beta" {
  project = var.project_id
  region  = var.region
}

# Variables
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name (production, staging, development)"
  type        = string
  default     = "production"
}

variable "service_name" {
  description = "Name of the service"
  type        = string
  default     = "congressional-api"
}

variable "database_password" {
  description = "Password for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Secret key for the API"
  type        = string
  sensitive   = true
}

# Enable required APIs
resource "google_project_service" "apis" {
  for_each = toset([
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "sql-component.googleapis.com",
    "sqladmin.googleapis.com",
    "redis.googleapis.com",
    "secretmanager.googleapis.com",
    "vpcaccess.googleapis.com"
  ])
  
  project = var.project_id
  service = each.value
  
  disable_on_destroy = false
}

# VPC for private resources
resource "google_compute_network" "vpc" {
  name                    = "${var.service_name}-vpc"
  auto_create_subnetworks = false
  
  depends_on = [google_project_service.apis]
}

resource "google_compute_subnetwork" "subnet" {
  name          = "${var.service_name}-subnet"
  ip_cidr_range = "10.0.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
  
  private_ip_google_access = true
}

# VPC Access Connector for Cloud Run
resource "google_vpc_access_connector" "connector" {
  name          = "${var.service_name}-connector"
  region        = var.region
  ip_cidr_range = "10.8.0.0/28"
  network       = google_compute_network.vpc.name
  
  depends_on = [google_project_service.apis]
}

# Cloud SQL PostgreSQL instance
resource "google_sql_database_instance" "postgres" {
  name             = "${var.service_name}-db"
  database_version = "POSTGRES_15"
  region           = var.region
  
  settings {
    tier              = "db-f1-micro"
    availability_type = "ZONAL"
    
    backup_configuration {
      enabled    = true
      start_time = "03:00"
      
      backup_retention_settings {
        retained_backups = 7
        retention_unit   = "COUNT"
      }
    }
    
    ip_configuration {
      ipv4_enabled    = false
      private_network = google_compute_network.vpc.id
    }
    
    database_flags {
      name  = "max_connections"
      value = "100"
    }
    
    database_flags {
      name  = "shared_preload_libraries"
      value = "pg_stat_statements"
    }
  }
  
  deletion_protection = true
  
  depends_on = [
    google_project_service.apis,
    google_service_networking_connection.private_vpc_connection
  ]
}

# Private service connection for Cloud SQL
resource "google_compute_global_address" "private_ip_address" {
  name          = "${var.service_name}-private-ip"
  purpose       = "VPC_PEERING"
  address_type  = "INTERNAL"
  prefix_length = 16
  network       = google_compute_network.vpc.id
}

resource "google_service_networking_connection" "private_vpc_connection" {
  network                 = google_compute_network.vpc.id
  service                 = "servicenetworking.googleapis.com"
  reserved_peering_ranges = [google_compute_global_address.private_ip_address.name]
}

# Database and user
resource "google_sql_database" "database" {
  name     = "congress_data"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "user" {
  name     = "congress_user"
  instance = google_sql_database_instance.postgres.name
  password = var.database_password
}

# Redis instance for caching
resource "google_redis_instance" "cache" {
  name           = "${var.service_name}-cache"
  memory_size_gb = 1
  region         = var.region
  
  authorized_network = google_compute_network.vpc.id
  
  redis_version = "REDIS_7_0"
  display_name  = "Congressional API Cache"
  
  depends_on = [google_project_service.apis]
}

# Secret Manager secrets
resource "google_secret_manager_secret" "database_url" {
  secret_id = "congressional-db-url"
  
  replication {
    automatic = true
  }
  
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_version" "database_url" {
  secret      = google_secret_manager_secret.database_url.id
  secret_data = "postgresql://${google_sql_user.user.name}:${var.database_password}@${google_sql_database_instance.postgres.private_ip_address}:5432/${google_sql_database.database.name}"
}

resource "google_secret_manager_secret" "secret_key" {
  secret_id = "congressional-secret-key"
  
  replication {
    automatic = true
  }
  
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_version" "secret_key" {
  secret      = google_secret_manager_secret.secret_key.id
  secret_data = var.secret_key
}

resource "google_secret_manager_secret" "redis_url" {
  secret_id = "congressional-redis-url"
  
  replication {
    automatic = true
  }
  
  depends_on = [google_project_service.apis]
}

resource "google_secret_manager_secret_version" "redis_url" {
  secret      = google_secret_manager_secret.redis_url.id
  secret_data = "redis://${google_redis_instance.cache.host}:${google_redis_instance.cache.port}/0"
}

# Service account for Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "${var.service_name}-run-sa"
  display_name = "Congressional API Cloud Run Service Account"
}

# IAM bindings for the service account
resource "google_project_iam_member" "cloud_run_sa_bindings" {
  for_each = toset([
    "roles/cloudsql.client",
    "roles/secretmanager.secretAccessor",
    "roles/redis.editor"
  ])
  
  project = var.project_id
  role    = each.value
  member  = "serviceAccount:${google_service_account.cloud_run_sa.email}"
}

# Cloud Run service
resource "google_cloud_run_service" "api" {
  name     = var.service_name
  location = var.region
  
  template {
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale"         = "10"
        "autoscaling.knative.dev/minScale"         = "1"
        "run.googleapis.com/vpc-access-connector"  = google_vpc_access_connector.connector.name
        "run.googleapis.com/vpc-access-egress"     = "private-ranges-only"
        "run.googleapis.com/execution-environment" = "gen2"
      }
    }
    
    spec {
      service_account_name = google_service_account.cloud_run_sa.email
      
      containers {
        image = "gcr.io/${var.project_id}/congressional-api:latest"
        
        ports {
          container_port = 8003
        }
        
        resources {
          limits = {
            cpu    = "2000m"
            memory = "1Gi"
          }
        }
        
        env {
          name  = "ENVIRONMENT"
          value = var.environment
        }
        
        env {
          name  = "LOG_LEVEL"
          value = "INFO"
        }
        
        env {
          name  = "DEBUG"
          value = "false"
        }
        
        env {
          name  = "API_HOST"
          value = "0.0.0.0"
        }
        
        env {
          name  = "API_PORT"
          value = "8003"
        }
        
        env {
          name = "DATABASE_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.database_url.secret_id
              key  = "latest"
            }
          }
        }
        
        env {
          name = "SECRET_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.secret_key.secret_id
              key  = "latest"
            }
          }
        }
        
        env {
          name = "REDIS_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.redis_url.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
  }
  
  traffic {
    percent         = 100
    latest_revision = true
  }
  
  depends_on = [google_project_service.apis]
}

# IAM policy for Cloud Run (allow public access)
resource "google_cloud_run_service_iam_member" "public_access" {
  service  = google_cloud_run_service.api.name
  location = google_cloud_run_service.api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

# Outputs
output "cloud_run_url" {
  description = "URL of the deployed Cloud Run service"
  value       = google_cloud_run_service.api.status[0].url
}

output "database_connection_name" {
  description = "The connection name of the database instance"
  value       = google_sql_database_instance.postgres.connection_name
}

output "redis_host" {
  description = "The host of the Redis instance"
  value       = google_redis_instance.cache.host
}

output "service_account_email" {
  description = "Email of the service account"
  value       = google_service_account.cloud_run_sa.email
}