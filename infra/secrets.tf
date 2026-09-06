data "aws_secretsmanager_secret" "supabase_url" {
  name = "${local.name}/SUPABASE_URL"
}

data "aws_secretsmanager_secret" "database_url" {
  name = "${local.name}/DATABASE_URL"
}

data "aws_secretsmanager_secret" "redis_url" {
  name = "${local.name}/REDIS_URL"
}

resource "aws_secretsmanager_secret_version" "redis_url" {
  secret_id     = data.aws_secretsmanager_secret.redis_url.id
  secret_string = "rediss://:${random_password.valkey_auth_token.result}@${module.valkey.replication_group_primary_endpoint_address}:6379/0"
}
