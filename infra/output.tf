output "api_alb_dns_name" {
  description = "Temporary API hostname. Point an API DNS record at this later."
  value       = module.alb.dns_name
}

output "api_base_url" {
  description = "Temporary API base URL for smoke tests."
  value       = "${lower(local.api_listener_protocol)}://${local.api_host}"
}

output "api_ws_url" {
  description = "Temporary WebSocket base URL for smoke tests."
  value       = "${local.api_uses_https ? "wss" : "ws"}://${local.api_host}/sessions"
}

output "frontend_bucket_name" {
  description = "S3 bucket where frontend/dist should be synced."
  value       = module.s3_bucket.s3_bucket_id
}

output "cloudfront_distribution_id" {
  description = "CloudFront distribution ID used for cache invalidations."
  value       = module.cloudfront.cloudfront_distribution_id
}

output "cloudfront_domain_name" {
  description = "Temporary frontend hostname."
  value       = module.cloudfront.cloudfront_distribution_domain_name
}

output "cloudfront_url" {
  description = "Temporary frontend URL."
  value       = "https://${module.cloudfront.cloudfront_distribution_domain_name}"
}

output "valkey_primary_endpoint" {
  description = "Valkey primary endpoint address."
  value       = module.valkey.replication_group_primary_endpoint_address
}

output "secret_names" {
  description = "Existing Secrets Manager secrets read by Terraform."
  value = {
    supabase_url = data.aws_secretsmanager_secret.supabase_url.name
    database_url = data.aws_secretsmanager_secret.database_url.name
    redis_url    = data.aws_secretsmanager_secret.redis_url.name
  }
}
