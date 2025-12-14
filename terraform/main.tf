terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Lambda Roles and Permissions
resource "aws_iam_role" "lambda_role" {
  name               = "gas_monitor_metadata"
  assume_role_policy = <<EOF

{
  "Version" : "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_policy" "iam_policy_for_lambda" {
  name = "gas_metadata_policy"
  path = "/"
  description = "AWS IAM Policy for managing lambda role"
  policy = <<EOF
{
  "Version" : "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
}

resource "aws_iam_role_policy_attachment" "s3_full_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "dynamodb_full_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess"
}

resource "aws_iam_role_policy_attachment" "cloudwatch_full_access" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchFullAccess"
}


# Bronze Lambda
data "archive_file" "bronze_zip" {
  type = "zip"
  source_dir = "${path.module}/lambdaBronze/python/"
  output_path = "${path.module}/lambdaBronze/python/metadataBronze.zip"
}

resource "aws_lambda_function" "bronze_metadata" {
  filename = "${path.module}/lambdaBronze/python/metadataBronze.zip"
  function_name = "bronzeMetadata"
  role = aws_iam_role.lambda_role.arn
  handler = "metadata.lambda_handler"
  runtime = "python3.10"
  timeout = 120
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}

resource "aws_lambda_permission" "allow_bronze_s3" {
  statement_id  = "AllowExecutionFromBronzeS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.bronze_metadata.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.gasMonitorsBronze.arn
}

resource "aws_s3_bucket_notification" "bronze_notifications" {
  bucket = aws_s3_bucket.gasMonitorsBronze.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.bronze_metadata.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_bronze_s3
  ]
}

# Silver Lambda
data "archive_file" "silver_zip" {
  type = "zip"
  source_dir = "${path.module}/lambdaSilver/python/"
  output_path = "${path.module}/lambdaSilver/python/metadataSilver.zip"
}

resource "aws_lambda_function" "silver_metadata" {
  filename = "${path.module}/lambdaSilver/python/metadataSilver.zip"
  function_name = "silverMetadata"
  role = aws_iam_role.lambda_role.arn
  handler = "metadata.lambda_handler"
  runtime = "python3.10"
  timeout = 120
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}

resource "aws_lambda_permission" "allow_silver_s3" {
  statement_id  = "AllowExecutionFromSilverS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.silver_metadata.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.gasMonitorsSilver.arn
}

resource "aws_s3_bucket_notification" "silver_notifications" {
  bucket = aws_s3_bucket.gasMonitorsSilver.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.silver_metadata.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_silver_s3
  ]
}

#Gold Lambda
data "archive_file" "gold_zip" {
  type = "zip"
  source_dir = "${path.module}/lambdaGold/python/"
  output_path = "${path.module}/lambdaGold/python/metadata.zip"
}

resource "aws_lambda_function" "gold_metadata" {
  filename = "${path.module}/lambdaGold/python/metadata.zip"
  function_name = "goldMetadata"
  role = aws_iam_role.lambda_role.arn
  handler = "metadata.lambda_handler"
  runtime = "python3.10"
  timeout = 120
  depends_on = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
}

resource "aws_lambda_permission" "allow_gold_s3" {
  statement_id  = "AllowExecutionFromGoldS3"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.gold_metadata.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.gasMonitorsGold.arn
}

resource "aws_s3_bucket_notification" "gold_notifications" {
  bucket = aws_s3_bucket.gasMonitorsGold.id

  lambda_function {
    lambda_function_arn = aws_lambda_function.gold_metadata.arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [
    aws_lambda_permission.allow_gold_s3
  ]
}