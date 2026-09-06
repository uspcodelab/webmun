# 1. S3 Bucket Module (Secure by default: public access blocked, encrypted)
module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 4.0"

  bucket        = var.frontend_bucket_name != null ? var.frontend_bucket_name : "${local.name}-frontend-assets-${var.aws_region}"
  force_destroy = var.frontend_bucket_force_destroy

  # Let CloudFront OAC read the bucket
  control_object_ownership = true
  object_ownership         = "BucketOwnerEnforced"

  # Automatically injects the CloudFront distribution ARN into the bucket policy
  attach_policy                         = true
  attach_deny_insecure_transport_policy = true
  attach_require_latest_tls_policy      = true
  policy                                = data.aws_iam_policy_document.s3_policy.json

  tags = local.tags
}

# 2. CloudFront Module (Handles OAC, distribution, and SPA error routing)
module "cloudfront" {
  source  = "terraform-aws-modules/cloudfront/aws"
  version = "~> 6.0"

  comment             = "Frontend SPA distribution"
  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"
  price_class         = var.cloudfront_price_class
  viewer_certificate = {
    cloudfront_default_certificate = true
  }

  origin_access_control = {
    s3_oac = {
      description      = "CloudFront access to S3 frontend bucket"
      origin_type      = "s3"
      signing_behavior = "always"
      signing_protocol = "sigv4"
    }
  }

  origin = {
    s3_frontend = {
      domain_name               = module.s3_bucket.s3_bucket_bucket_regional_domain_name
      origin_access_control_key = "s3_oac"
    }
  }

  default_cache_behavior = {
    target_origin_id       = "s3_frontend"
    viewer_protocol_policy = "redirect-to-https"
    allowed_methods        = ["GET", "HEAD", "OPTIONS"]
    cached_methods         = ["GET", "HEAD"]
    use_forwarded_values   = false

    # AWS Managed CachingOptimized policy
    cache_policy_id = "658327ea-f89d-4fab-a63d-7e88639e58f6"
  }

  # SPA Routing (403 and 404 redirected to index.html with HTTP 200)
  custom_error_response = [
    {
      error_code         = 403
      response_code      = 200
      response_page_path = "/index.html"
    },
    {
      error_code         = 404
      response_code      = 200
      response_page_path = "/index.html"
    }
  ]

  tags = local.tags
}

# 3. Grant CloudFront OAC permission to read S3 objects
data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions   = ["s3:GetObject"]
    resources = ["${module.s3_bucket.s3_bucket_arn}/*"]

    principals {
      type        = "Service"
      identifiers = ["cloudfront.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "AWS:SourceArn"
      values   = [module.cloudfront.cloudfront_distribution_arn]
    }
  }
}
