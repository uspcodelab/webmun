variable "project_name" {
  description = "Short project name used in AWS resource names."
  type        = string
  default     = "webmun"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "The AWS region to deploy resources in"
  type        = string
  default     = "sa-east-1"
}

variable "az_count" {
  description = "Number of availability zones/public subnets to create."
  type        = number
  default     = 2
}

variable "vpc_cidr" {
  description = "IPv4 CIDR block for the VPC."
  type        = string
  default     = "10.0.0.0/16"
}

variable "api_certificate_arn" {
  description = "Optional ACM certificate ARN for the API ALB HTTPS listener. Leave null for HTTP smoke tests."
  type        = string
  default     = null
}

variable "api_domain_name" {
  description = "Optional custom API hostname, for example api.webmun.net. Used in outputs after DNS points to the ALB."
  type        = string
  default     = null
}

variable "backend_image" {
  description = "Container image used by the ECS backend service."
  type        = string
  default     = "r0liveir/webmun-backend-app:latest"
}

variable "backend_cpu" {
  description = "Fargate CPU units for the backend task."
  type        = number
  default     = 256
}

variable "backend_memory" {
  description = "Fargate memory in MiB for the backend task."
  type        = number
  default     = 512
}

variable "backend_log_level" {
  description = "Backend LOG_LEVEL value."
  type        = string
  default     = "INFO"
}

variable "backend_log_retention_days" {
  description = "CloudWatch log retention for backend container logs."
  type        = number
  default     = 7
}

variable "cors_origins" {
  description = "Comma-separated frontend origins allowed by the backend."
  type        = string

  validation {
    condition = alltrue([
      for origin in split(",", var.cors_origins) :
      can(regex("^https?://", trimspace(origin)))
    ])
    error_message = "Each CORS origin must include http:// or https://, for example https://d111111abcdef8.cloudfront.net."
  }
}

variable "valkey_node_type" {
  description = "ElastiCache node size for Valkey."
  type        = string
  default     = "cache.t4g.micro"
}

variable "frontend_bucket_name" {
  description = "Optional exact bucket name for frontend build artifacts. S3 bucket names are globally unique."
  type        = string
  default     = null
}

variable "frontend_bucket_force_destroy" {
  description = "Allow Terraform to delete the frontend bucket even when it contains files."
  type        = bool
  default     = false
}

variable "cloudfront_price_class" {
  description = "CloudFront edge location price class."
  type        = string
  default     = "PriceClass_100"
}
