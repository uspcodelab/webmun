module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 6.0"

  name = local.name
  cidr = var.vpc_cidr

  azs            = local.azs
  public_subnets = [for index, _ in local.azs : cidrsubnet(var.vpc_cidr, 8, index)]

  enable_dns_hostnames = true
  enable_dns_support   = true
  enable_nat_gateway   = false

  tags = local.tags
}
