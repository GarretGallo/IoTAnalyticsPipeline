data "aws_iam_policy_document" "DBS3" {
  statement {
    effect = "Allow"

    actions = [
      "s3:ListBucket",
    ]

    resources = [
      "arn:aws:s3:::gasmonitorsbronze",
      "arn:aws:s3:::gasmonitorssilver",
      "arn:aws:s3:::gasmonitorsgold",
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]

    resources = [
      "arn:aws:s3:::gasmonitorsbronze/*",
      "arn:aws:s3:::gasmonitorssilver/*",
      "arn:aws:s3:::gasmonitorsgold/*",
    ]
  }
}

resource "aws_iam_policy" "databricks_s3_policy" {
  name   = "databricks-s3-access-policy"
  policy = data.aws_iam_policy_document.DBS3.json
}

resource "aws_iam_role" "databricksS3access" {
  name               = "databricks-s3-access-role"
  assume_role_policy = data.aws_iam_policy_document.DBS3.json
}