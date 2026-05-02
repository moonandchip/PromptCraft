resource "aws_security_group" "app" {
  name        = "${local.name_prefix}-app"
  description = "Ingress for ${local.name_prefix} app stack"
  vpc_id      = data.aws_vpc.default.id

  # All outbound — instance pulls images from GHCR, hits Leonardo / OpenAI,
  # writes to CloudWatch Logs.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTP — needed for Let's Encrypt HTTP-01 challenges; Caddy redirects
  # everything else to HTTPS.
  ingress {
    description = "HTTP (ACME challenges + redirect)"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP/3 (QUIC)"
    from_port   = 443
    to_port     = 443
    protocol    = "udp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # SSH only if explicit CIDRs were provided. Empty list = no rule = SSM only.
  dynamic "ingress" {
    for_each = toset(var.ssh_allowed_cidrs)
    content {
      description = "SSH"
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = [ingress.value]
    }
  }
}
