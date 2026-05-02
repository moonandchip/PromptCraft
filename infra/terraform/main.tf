################################################################################
# Cross-variable validation
################################################################################

resource "null_resource" "validate_hostnames" {
  lifecycle {
    precondition {
      condition     = !(var.use_sslip && var.domain_name != "")
      error_message = "Set EITHER use_sslip = true OR domain_name = '<domain>', not both."
    }
  }
}

################################################################################
# Locals
################################################################################

locals {
  name_prefix = "${var.project_name}-${var.environment}"

  # sslip.io derives a DNS name from the EIP: 34.1.2.3 -> 34-1-2-3.sslip.io
  sslip_base = "${replace(aws_eip.app.public_ip, ".", "-")}.sslip.io"

  # Hostnames the app is served at. Empty string when neither sslip nor domain
  # is configured (the stack still runs, just plain HTTP on the EIP).
  api_host = (
    var.use_sslip ? "api.${local.sslip_base}" :
    var.domain_name != "" ? "api.${var.domain_name}" :
    ""
  )
  auth_host = (
    var.use_sslip ? "auth.${local.sslip_base}" :
    var.domain_name != "" ? "auth.${var.domain_name}" :
    ""
  )

  use_tls = var.use_sslip || var.domain_name != ""

  # Public URLs (https when TLS is on, http://EIP fallback otherwise — only
  # used for local sanity checks; production must have TLS).
  api_url  = local.use_tls ? "https://${local.api_host}" : "http://${aws_eip.app.public_ip}"
  auth_url = local.use_tls ? "https://${local.auth_host}" : "http://${aws_eip.app.public_ip}"

  # CORS origins for the backend. Joins the Vercel frontend origin with any
  # extras (preview deploys etc.). Comma-separated for the Python settings.
  cors_origins_list = compact(concat(
    [var.frontend_origin],
    var.cors_extra_origins,
  ))
  cors_allowed_origins = join(",", local.cors_origins_list)

  # Lowercased GHCR repo path. GHCR rejects uppercase in image references.
  github_repository_lc = lower(var.github_repository)

  # Rendered config files. user-data writes these to /etc/promptcraft/.
  env_file = templatefile("${path.module}/files/env.tftpl", {
    db_password           = var.db_password
    auth_secret           = var.auth_secret
    auth_url              = local.use_tls ? local.auth_url : "http://localhost:3000"
    leonardo_api_key      = var.leonardo_api_key
    openai_api_key        = var.openai_api_key
    prompt_feedback_model = var.prompt_feedback_model
    cors_allowed_origins  = local.cors_allowed_origins
  })

  compose_file = templatefile("${path.module}/files/docker-compose.yml.tftpl", {
    aws_region        = var.aws_region
    log_group         = aws_cloudwatch_log_group.app.name
    github_repository = local.github_repository_lc
    image_tag         = var.image_tag
  })

  caddy_file = templatefile("${path.module}/files/Caddyfile.tftpl", {
    use_tls    = local.use_tls
    api_host   = local.api_host
    auth_host  = local.auth_host
    acme_email = var.acme_email
  })

  init_db_sql = file("${path.module}/files/init-db.sql")

  user_data = templatefile("${path.module}/files/user-data.sh.tftpl", {
    project_name  = var.project_name
    env_file      = local.env_file
    compose_file  = local.compose_file
    caddy_file    = local.caddy_file
    init_db_sql   = local.init_db_sql
    ghcr_username = var.ghcr_username
    ghcr_token    = var.ghcr_token
  })
}

################################################################################
# Data sources — default VPC / subnets / Ubuntu AMI
################################################################################

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Pin to the first AZ in the region. The data EBS volume must live in the
# same AZ as the instance, so we choose one and stick with it.
data "aws_subnet" "primary" {
  id = sort(data.aws_subnets.default.ids)[0]
}

data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"] # Canonical

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}
