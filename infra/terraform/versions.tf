terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    key     = "main/terraform.tfstate"
    encrypt = true
    # bucket, region, dynamodb_table are passed via -backend-config flags
    # at init time (see backend.hcl.example and infra.yml workflow).
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.60"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}
