# Infrastructure folder

Prerequisites: Terraform, AWS CLI, Docker, and npm.

Terraform provisions the AWS infrastructure for the FastAPI backend and the
React frontend. Configure AWS credentials before running these commands.

## Setup

Create these plaintext secrets in AWS Secrets Manager before the first apply:

```text
webmun-prod/SUPABASE_URL
webmun-prod/DATABASE_URL
webmun-prod/REDIS_URL
```

Then initialize and apply the infrastructure:

```bash
cd infra
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

Keep `terraform.tfvars`, `.terraform/`, and Terraform state files local. Commit
`.terraform.lock.hcl` so provider versions remain reproducible.

## Deploy backend

Build and push the production image configured by `backend_image`:

```bash
docker build --target production -t r0liveir/webmun-backend-app:latest backend
docker push r0liveir/webmun-backend-app:latest
```

When reusing the `latest` tag, restart the ECS service so it pulls the new image:

```bash
aws ecs update-service \
  --region sa-east-1 \
  --cluster webmun-prod-cluster \
  --service backend \
  --force-new-deployment
```

Prefer immutable image tags for releases. Update `backend_image` in
`terraform.tfvars` and run `terraform apply` when changing the tag.

## Deploy frontend

Build the static frontend with the production endpoints:

```bash
cd frontend
VITE_API_URL="$(cd ../infra && terraform output -raw api_base_url)" \
VITE_WS_URL="$(cd ../infra && terraform output -raw api_ws_url)" \
VITE_SUPABASE_URL="https://your-project.supabase.co" \
VITE_SUPABASE_PUBLISHABLE_KEY="your-supabase-publishable-key" \
npm run build
```

Upload it to S3 and invalidate CloudFront:

```bash
aws s3 sync dist/ "s3://$(cd ../infra && terraform output -raw frontend_bucket_name)" --delete
aws cloudfront create-invalidation \
  --distribution-id "$(cd ../infra && terraform output -raw cloudfront_distribution_id)" \
  --paths "/*"
```

When the frontend origin changes, update `cors_origins` in `terraform.tfvars`
and run `terraform apply`.

## Update backend secrets

Update secret values directly in AWS Secrets Manager. ECS reads them when a
task starts, so force a new backend deployment after every secret change.
