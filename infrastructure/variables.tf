variable "db_username" {
  description = "The username for the PostgreSQL database"
  type        = string
}

variable "db_password" {
  description = "The password for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "The AWS region"
  type        = string
  default     = "us-east-1"
}
