terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
  }

  # Local backend by design. This module's whole job is to create the
  # remote backend (S3 + DynamoDB) that infra/terraform/ uses. Its own
  # state stays on disk and out of git (see .gitignore).
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project   = var.project_name
      ManagedBy = "terraform-bootstrap"
    }
  }
}

data "aws_caller_identity" "current" {}
