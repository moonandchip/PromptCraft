resource "aws_iam_openid_connect_provider" "github" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]

  # GitHub's OIDC root cert thumbprints. AWS now validates the cert chain
  # itself, so these are belt-and-suspenders and rarely need updating.
  thumbprint_list = [
    "6938fd4d98bab03faadb97b34396831e3780aea1",
    "1c58a3a8518e8759bf075b76b750d4f2df264fcd",
  ]
}

data "aws_iam_policy_document" "gh_actions_assume" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    # Allows pushes to main (apply) and pull requests (plan only).
    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values = [
        "repo:${var.github_repo}:ref:refs/heads/main",
        "repo:${var.github_repo}:pull_request",
      ]
    }
  }
}

resource "aws_iam_role" "gh_actions" {
  name               = "${var.project_name}-github-actions"
  assume_role_policy = data.aws_iam_policy_document.gh_actions_assume.json
}

# ---------------------------------------------------------------------------
# Terraform state access — scoped to the exact bucket and lock table.
# ---------------------------------------------------------------------------
data "aws_iam_policy_document" "tf_state" {
  statement {
    actions = [
      "s3:ListBucket",
      "s3:GetBucketVersioning",
    ]
    resources = [aws_s3_bucket.tf_state.arn]
  }

  statement {
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]
    resources = ["${aws_s3_bucket.tf_state.arn}/*"]
  }

  statement {
    actions = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:DeleteItem",
      "dynamodb:DescribeTable",
    ]
    resources = [aws_dynamodb_table.tf_lock.arn]
  }
}

resource "aws_iam_role_policy" "tf_state" {
  name   = "tf-state"
  role   = aws_iam_role.gh_actions.id
  policy = data.aws_iam_policy_document.tf_state.json
}

# ---------------------------------------------------------------------------
# Project resource management. EC2 (incl. EBS, EIP, SG, key pair) is broad
# but blast radius is fine: only this repo on main/PR can assume the role.
# ---------------------------------------------------------------------------
resource "aws_iam_role_policy_attachment" "ec2_full" {
  role       = aws_iam_role.gh_actions.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

# IAM management — scoped to resources prefixed with the project name so
# the CI role can't touch unrelated roles or instance profiles.
data "aws_iam_policy_document" "iam_management" {
  statement {
    actions = [
      "iam:CreateRole",
      "iam:DeleteRole",
      "iam:GetRole",
      "iam:UpdateRole",
      "iam:UpdateAssumeRolePolicy",
      "iam:ListRolePolicies",
      "iam:ListAttachedRolePolicies",
      "iam:PutRolePolicy",
      "iam:DeleteRolePolicy",
      "iam:GetRolePolicy",
      "iam:AttachRolePolicy",
      "iam:DetachRolePolicy",
      "iam:CreateInstanceProfile",
      "iam:DeleteInstanceProfile",
      "iam:GetInstanceProfile",
      "iam:AddRoleToInstanceProfile",
      "iam:RemoveRoleFromInstanceProfile",
      "iam:PassRole",
      "iam:TagRole",
      "iam:UntagRole",
      "iam:ListRoleTags",
      "iam:TagInstanceProfile",
      "iam:UntagInstanceProfile",
      "iam:ListInstanceProfileTags",
      "iam:ListInstanceProfilesForRole",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${var.project_name}-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/${var.project_name}-*",
    ]
  }
}

resource "aws_iam_role_policy" "iam_management" {
  name   = "iam-management"
  role   = aws_iam_role.gh_actions.id
  policy = data.aws_iam_policy_document.iam_management.json
}

# CloudWatch Logs — scoped to /promptcraft/*
data "aws_iam_policy_document" "logs_management" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:DeleteLogGroup",
      "logs:DescribeLogGroups",
      "logs:PutRetentionPolicy",
      "logs:DeleteRetentionPolicy",
      "logs:TagResource",
      "logs:UntagResource",
      "logs:ListTagsForResource",
    ]
    resources = [
      "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/${var.project_name}/*",
      "arn:aws:logs:${var.aws_region}:${data.aws_caller_identity.current.account_id}:log-group:/${var.project_name}/*:log-stream:*",
    ]
  }

  # DescribeLogGroups requires "*" — there's no resource-level filter for it.
  statement {
    actions   = ["logs:DescribeLogGroups"]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "logs_management" {
  name   = "logs-management"
  role   = aws_iam_role.gh_actions.id
  policy = data.aws_iam_policy_document.logs_management.json
}

# SSM SendCommand — used by ci-cd.yml to trigger `docker compose pull && up -d`
# on the EC2 instance. Scoped to "*" because the instance ID isn't known here;
# the OIDC sub claim already gates who can use it.
data "aws_iam_policy_document" "ssm_deploy" {
  statement {
    actions = [
      "ssm:SendCommand",
      "ssm:GetCommandInvocation",
      "ssm:ListCommandInvocations",
      "ssm:DescribeInstanceInformation",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_role_policy" "ssm_deploy" {
  name   = "ssm-deploy"
  role   = aws_iam_role.gh_actions.id
  policy = data.aws_iam_policy_document.ssm_deploy.json
}
