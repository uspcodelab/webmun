module "ecs" {
  source  = "terraform-aws-modules/ecs/aws"
  version = "~> 7.0"

  cluster_name = "${local.name}-cluster"

  services = {
    backend = {
      cpu    = var.backend_cpu
      memory = var.backend_memory

      container_definitions = {
        backend = {
          image     = var.backend_image
          essential = true
          portMappings = [
            {
              name          = "http"
              containerPort = 8000
              protocol      = "tcp"
            }
          ]

          environment = [
            { name = "ENVIRONMENT", value = "production" },
            { name = "LOG_LEVEL", value = var.backend_log_level },
            { name = "CORS_ORIGINS", value = var.cors_origins },
            { name = "PORT", value = "8000" }
          ]

          secrets = [
            { name = "SUPABASE_URL", valueFrom = data.aws_secretsmanager_secret.supabase_url.arn },
            { name = "DATABASE_URL", valueFrom = data.aws_secretsmanager_secret.database_url.arn },
            { name = "REDIS_URL", valueFrom = data.aws_secretsmanager_secret.redis_url.arn }
          ]

          enable_cloudwatch_logging              = true
          create_cloudwatch_log_group            = true
          cloudwatch_log_group_retention_in_days = var.backend_log_retention_days
        }
      }

      assign_public_ip = true
      subnet_ids       = module.vpc.public_subnets

      load_balancer = {
        service = {
          target_group_arn = module.alb.target_groups["backend"].arn
          container_name   = "backend"
          container_port   = 8000
        }
      }

      task_exec_secret_arns = [
        data.aws_secretsmanager_secret.supabase_url.arn,
        data.aws_secretsmanager_secret.database_url.arn,
        data.aws_secretsmanager_secret.redis_url.arn
      ]

      security_group_ingress_rules = {
        ingress_alb = {
          from_port                    = 8000
          to_port                      = 8000
          ip_protocol                  = "tcp"
          description                  = "Backend HTTP from the ALB only"
          referenced_security_group_id = module.alb.security_group_id
        }
      }

      security_group_egress_rules = {
        egress_all = {
          ip_protocol = "-1"
          description = "Backend outbound internet and VPC traffic"
          cidr_ipv4   = "0.0.0.0/0"
        }
      }
    }
  }

  tags = local.tags
}
