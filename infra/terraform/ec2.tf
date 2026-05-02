################################################################################
# Optional admin key pair (only created when ssh_public_key is non-empty)
################################################################################

resource "aws_key_pair" "admin" {
  count      = var.ssh_public_key != "" ? 1 : 0
  key_name   = "${local.name_prefix}-admin"
  public_key = var.ssh_public_key
}

################################################################################
# EBS volume for Postgres data — separate from instance lifecycle
################################################################################

resource "aws_ebs_volume" "postgres" {
  availability_zone = data.aws_subnet.primary.availability_zone
  size              = var.data_volume_size_gb
  type              = "gp3"
  encrypted         = true

  tags = {
    Name = "${local.name_prefix}-postgres"
  }

  lifecycle {
    # Don't ever destroy this volume — it holds the database. To delete,
    # remove this block and `terraform destroy` deliberately.
    prevent_destroy = true
  }
}

################################################################################
# Elastic IP — allocated separately so user_data can reference its address
# without creating a circular dependency on the instance.
################################################################################

resource "aws_eip" "app" {
  domain = "vpc"

  tags = {
    Name = "${local.name_prefix}-app"
  }
}

################################################################################
# EC2 instance
################################################################################

resource "aws_instance" "app" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = var.instance_type
  subnet_id                   = data.aws_subnet.primary.id
  vpc_security_group_ids      = [aws_security_group.app.id]
  iam_instance_profile        = aws_iam_instance_profile.app.name
  key_name                    = var.ssh_public_key != "" ? aws_key_pair.admin[0].key_name : null
  associate_public_ip_address = true

  user_data                   = local.user_data
  user_data_replace_on_change = true

  metadata_options {
    http_tokens = "required" # IMDSv2
  }

  root_block_device {
    volume_size = var.root_volume_size_gb
    volume_type = "gp3"
    encrypted   = true
  }

  tags = {
    Name = "${local.name_prefix}-app"
  }

  lifecycle {
    # New Canonical AMI revisions shouldn't trigger replacement on every
    # apply. To rebuild the box on a fresh AMI, taint or `-replace=`.
    ignore_changes = [ami]
  }

  depends_on = [aws_cloudwatch_log_group.app]
}

resource "aws_volume_attachment" "postgres" {
  device_name = "/dev/sdh"
  volume_id   = aws_ebs_volume.postgres.id
  instance_id = aws_instance.app.id

  # Force-detach on instance replacement so the new instance can attach.
  force_detach = true
}

resource "aws_eip_association" "app" {
  instance_id   = aws_instance.app.id
  allocation_id = aws_eip.app.id
}
