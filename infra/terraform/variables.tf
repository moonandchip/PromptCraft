################################################################################
# Project / environment
################################################################################

variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Short slug for resource names and tags."
  type        = string
  default     = "promptcraft"
}

variable "environment" {
  description = "Environment slug (prod, staging). Joined into the EC2 Name tag and CloudWatch log group."
  type        = string
  default     = "prod"
}

################################################################################
# Compute
################################################################################

variable "instance_type" {
  description = "EC2 instance type. t3.small is sized for ~25 concurrent users with CLIP-on-demand. Bump to t3.medium if OOM occurs."
  type        = string
  default     = "t3.small"
}

variable "root_volume_size_gb" {
  description = "Root EBS volume size. Holds Docker images + OS."
  type        = number
  default     = 20
}

variable "data_volume_size_gb" {
  description = "Postgres data EBS volume size. Survives instance replacement."
  type        = number
  default     = 20
}

variable "ssh_public_key" {
  description = "SSH public key (OpenSSH format, single line). Empty string skips key pair creation. SSM Session Manager works without SSH."
  type        = string
  default     = ""
  sensitive   = true
}

variable "ssh_allowed_cidrs" {
  description = "CIDR blocks permitted SSH (port 22) ingress. Empty list means no SSH access; use SSM Session Manager."
  type        = list(string)
  default     = []
}

################################################################################
# GHCR / images
################################################################################

variable "github_repository" {
  description = "GitHub repository in 'owner/repo' form. Used to construct GHCR image paths (lowercased)."
  type        = string

  validation {
    condition     = can(regex("^[^/]+/[^/]+$", var.github_repository))
    error_message = "github_repository must be 'owner/repo' (e.g. 'mateuszbobkowski49/PromptCraft')."
  }
}

variable "ghcr_username" {
  description = "GitHub username used by the EC2 instance to docker-login to ghcr.io."
  type        = string
}

variable "ghcr_token" {
  description = "GitHub PAT or fine-grained token with read:packages scope. Used by the EC2 to pull private GHCR images."
  type        = string
  sensitive   = true
}

variable "image_tag" {
  description = "GHCR image tag for backend / auth / frontend (frontend image isn't deployed here, frontend lives on Vercel)."
  type        = string
  default     = "latest"
}

################################################################################
# Hostnames / TLS
################################################################################

variable "domain_name" {
  description = "Apex domain (e.g. 'promptcrafts.net'). The stack serves api.<domain> and auth.<domain>. Empty string disables TLS."
  type        = string
  default     = ""
}

variable "use_sslip" {
  description = "Use sslip.io hostnames derived from the EIP (api.34-1-2-3.sslip.io). Lets you stand up TLS before owning a domain. Mutually exclusive with domain_name."
  type        = bool
  default     = false
}

variable "acme_email" {
  description = "Email for Let's Encrypt expiry notices. Empty uses Caddy's default ZeroSSL flow."
  type        = string
  default     = ""
}

variable "route53_zone_id" {
  description = "Route53 hosted zone ID for var.domain_name. Empty string skips DNS record creation (manage records at your registrar)."
  type        = string
  default     = ""
}

################################################################################
# App config
################################################################################

variable "frontend_origin" {
  description = "Vercel origin (e.g. 'https://promptcrafts.net'). Added to CORS_ALLOWED_ORIGINS on the backend."
  type        = string
  default     = ""
}

variable "cors_extra_origins" {
  description = "Extra origins to allow in CORS (e.g. preview deploys). Joined with frontend_origin."
  type        = list(string)
  default     = []
}

variable "prompt_feedback_model" {
  description = "OpenAI model name for prompt feedback."
  type        = string
  default     = "gpt-4.1-mini"
}

################################################################################
# Secrets
################################################################################

variable "db_password" {
  description = "Postgres password for the postgres superuser. Used in DATABASE_URL and AUTH_DATABASE_URL — only A-Za-z0-9_- to avoid URL-encoding."
  type        = string
  sensitive   = true

  validation {
    condition     = can(regex("^[A-Za-z0-9_-]+$", var.db_password)) && length(var.db_password) >= 16
    error_message = "db_password must be >= 16 chars and only A-Z, a-z, 0-9, _, - (avoids URL-reserved chars in DATABASE_URL)."
  }
}

variable "auth_secret" {
  description = "HMAC secret for next-auth + the /api/internal/* tokens. >= 32 chars random."
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.auth_secret) >= 32
    error_message = "auth_secret must be at least 32 characters."
  }
}

variable "leonardo_api_key" {
  description = "Leonardo AI API key for image generation."
  type        = string
  sensitive   = true
}

variable "openai_api_key" {
  description = "OpenAI API key for prompt feedback. Empty string disables feedback (backend swallows the missing key)."
  type        = string
  default     = ""
  sensitive   = true
}

################################################################################
# Logging
################################################################################

variable "log_retention_days" {
  description = "CloudWatch log retention."
  type        = number
  default     = 30
}
