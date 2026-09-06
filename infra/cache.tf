resource "random_password" "valkey_auth_token" {
  length  = 48
  special = false
}

module "valkey" {
  source  = "terraform-aws-modules/elasticache/aws"
  version = "~> 1.0"

  replication_group_id = "${local.name}-cache"
  description          = "WebMUN Redis-compatible Valkey cache"

  engine         = "valkey"
  engine_version = "7.2"
  node_type      = var.valkey_node_type

  automatic_failover_enabled = false
  multi_az_enabled           = false
  transit_encryption_enabled = true
  auth_token                 = random_password.valkey_auth_token.result
  apply_immediately          = true

  vpc_id = module.vpc.vpc_id
  security_group_rules = {
    ingress_from_backend = {
      description                  = "Valkey from ECS backend tasks"
      from_port                    = 6379
      to_port                      = 6379
      ip_protocol                  = "tcp"
      referenced_security_group_id = module.ecs.services["backend"].security_group_id
    }
  }

  subnet_group_name        = "${local.name}-cache"
  subnet_group_description = "Public subnet group for first-pass WebMUN Valkey"
  subnet_ids               = module.vpc.public_subnets

  create_parameter_group      = true
  parameter_group_name        = "${local.name}-cache"
  parameter_group_family      = "valkey7"
  parameter_group_description = "WebMUN Valkey parameters"

  tags = local.tags
}
