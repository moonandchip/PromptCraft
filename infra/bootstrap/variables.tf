variable "aws_region" {
  description = "AWS region for state bucket, lock table, and the eventual app stack."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Short slug used in resource names and tags."
  type        = string
  default     = "promptcraft"
}

variable "github_repo" {
  description = "GitHub repository in 'owner/repo' format. Scopes which repo can assume the CI role via OIDC."
  type        = string

  validation {
    condition     = can(regex("^[^/]+/[^/]+$", var.github_repo))
    error_message = "github_repo must be in the form 'owner/repo' (e.g. 'mateuszbobkowski49/PromptCraft')."
  }
}
