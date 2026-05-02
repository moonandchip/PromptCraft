################################################################################
# Optional Route53 A records — only created when domain_name AND
# route53_zone_id are both set. With an external registrar (Namecheap,
# GoDaddy, etc.) leave route53_zone_id empty and create the records
# manually pointing api.<domain> + auth.<domain> at the EIP output.
################################################################################

resource "aws_route53_record" "api" {
  count   = var.domain_name != "" && var.route53_zone_id != "" ? 1 : 0
  zone_id = var.route53_zone_id
  name    = local.api_host
  type    = "A"
  ttl     = 300
  records = [aws_eip.app.public_ip]
}

resource "aws_route53_record" "auth" {
  count   = var.domain_name != "" && var.route53_zone_id != "" ? 1 : 0
  zone_id = var.route53_zone_id
  name    = local.auth_host
  type    = "A"
  ttl     = 300
  records = [aws_eip.app.public_ip]
}
