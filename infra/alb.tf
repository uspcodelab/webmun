module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 10.0"

  name               = "${local.name}-api"
  load_balancer_type = "application"

  vpc_id  = module.vpc.vpc_id
  subnets = module.vpc.public_subnets

  enable_deletion_protection = false

  security_group_ingress_rules = {
    api = {
      from_port   = local.api_listener_port
      to_port     = local.api_listener_port
      ip_protocol = "tcp"
      cidr_ipv4   = "0.0.0.0/0"
      description = "${local.api_listener_protocol} from the internet"
    }
  }

  security_group_egress_rules = {
    all = {
      ip_protocol = "-1"
      cidr_ipv4   = "0.0.0.0/0"
      description = "Allow ALB outbound traffic to ECS tasks"
    }
  }

  listeners = {
    api = {
      port            = local.api_listener_port
      protocol        = local.api_listener_protocol
      certificate_arn = local.api_listener_protocol == "HTTPS" ? var.api_certificate_arn : null

      forward = {
        target_group_key = "backend"
      }
    }
  }

  target_groups = {
    backend = {
      name_prefix                       = "api-"
      protocol                          = "HTTP"
      port                              = 8000
      target_type                       = "ip"
      deregistration_delay              = 30
      create_attachment                 = false
      load_balancing_cross_zone_enabled = true

      health_check = {
        enabled             = true
        interval            = 30
        path                = "/docs"
        healthy_threshold   = 2
        unhealthy_threshold = 3
        timeout             = 5
        protocol            = "HTTP"
        matcher             = "200-399"
      }
    }
  }

  tags = local.tags
}
