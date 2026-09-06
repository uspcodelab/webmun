terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 6.41, < 7.0"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 3.0, < 4.0"
    }
  }

  required_version = ">= 1.5.7"
}

provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {
  state = "available"
}

locals {
  name                  = "${var.project_name}-${var.environment}"
  azs                   = slice(data.aws_availability_zones.available.names, 0, var.az_count)
  api_uses_https        = var.api_certificate_arn != null && var.api_certificate_arn != ""
  api_listener_port     = local.api_uses_https ? 443 : 80
  api_listener_protocol = local.api_uses_https ? "HTTPS" : "HTTP"
  api_host              = var.api_domain_name != null && var.api_domain_name != "" ? var.api_domain_name : module.alb.dns_name

  tags = {
    Project     = var.project_name
    Environment = var.environment
    Terraform   = "true"
  }
}
