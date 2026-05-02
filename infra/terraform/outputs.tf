output "public_ip" {
  description = "Elastic IP. Point api.<domain> and auth.<domain> A records here at your registrar."
  value       = aws_eip.app.public_ip
}

output "instance_id" {
  description = "EC2 instance ID."
  value       = aws_instance.app.id
}

output "api_url" {
  description = "Public URL for the FastAPI backend."
  value       = local.api_url
}

output "auth_url" {
  description = "Public URL for the Next.js auth service."
  value       = local.auth_url
}

output "vercel_env_vars" {
  description = "Paste these into the Vercel project's Production environment variables."
  value = {
    VITE_API_URL  = local.api_url
    VITE_AUTH_URL = local.auth_url
  }
}

output "ssm_session_command" {
  description = "Open a shell on the EC2 instance via SSM (no SSH needed)."
  value       = "aws ssm start-session --region ${var.aws_region} --target ${aws_instance.app.id}"
}

output "log_group_name" {
  description = "CloudWatch log group containing all four container streams."
  value       = aws_cloudwatch_log_group.app.name
}

output "dns_records_to_create" {
  description = "Records to create at your domain registrar (only relevant when domain_name is set and route53_zone_id is empty)."
  value = (
    var.domain_name == "" || var.route53_zone_id != "" ? null : {
      "api.${var.domain_name}"  = "A ${aws_eip.app.public_ip}"
      "auth.${var.domain_name}" = "A ${aws_eip.app.public_ip}"
    }
  )
}
