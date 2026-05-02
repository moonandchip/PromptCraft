output "github_actions_role_arn" {
  description = "Set as GitHub repo Variable: AWS_ROLE_ARN"
  value       = aws_iam_role.gh_actions.arn
}

output "tf_state_bucket" {
  description = "Set as GitHub repo Variable: TF_STATE_BUCKET"
  value       = aws_s3_bucket.tf_state.id
}

output "tf_lock_table" {
  description = "Set as GitHub repo Variable: TF_LOCK_TABLE"
  value       = aws_dynamodb_table.tf_lock.name
}

output "aws_region" {
  description = "Set as GitHub repo Variable: AWS_REGION"
  value       = var.aws_region
}

output "next_steps" {
  description = "What to do after this apply succeeds."
  value       = <<-EOT

    Bootstrap complete. Next steps:

    1. In GitHub repo Settings -> Secrets and variables -> Actions, add these
       four Variables (not secrets):
         AWS_ROLE_ARN     = ${aws_iam_role.gh_actions.arn}
         TF_STATE_BUCKET  = ${aws_s3_bucket.tf_state.id}
         TF_LOCK_TABLE    = ${aws_dynamodb_table.tf_lock.name}
         AWS_REGION       = ${var.aws_region}

    2. Tell me to start phase 2 and I'll write infra/terraform/ + the
       infra.yml workflow that uses this role.
  EOT
}
