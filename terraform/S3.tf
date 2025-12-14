resource "aws_s3_bucket" "gasMonitorsBronze" {
  bucket = "gasmonitorsbronze"

  tags = {
    Product = "gas-monitors"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "gasMonitorsBronzeLCP" {
  bucket = aws_s3_bucket.gasMonitorsBronze.id

  rule {
    id = "rule-1"

    filter {
      prefix = ""
    }

    transition {
      days = 180
      storage_class = "STANDARD_IA"
    }

    transition {
      days = 366
      storage_class = "GLACIER"
    }
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "gasMonitorsSilver" {
  bucket = "gasmonitorssilver"

  tags = {
    Product = "gas-monitors"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "gasMonitorsSilverLCP" {
  bucket = aws_s3_bucket.gasMonitorsSilver.id

  rule {
    id = "rule-1"

    filter {
      prefix = ""
    }

    transition {
      days = 180
      storage_class = "STANDARD_IA"
    }

    transition {
      days = 366
      storage_class = "GLACIER"
    }
    status = "Enabled"
  }
}

resource "aws_s3_bucket" "gasMonitorsGold" {
  bucket = "gasmonitorsgold"

  tags = {
    Product = "gas-monitors"
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "gasMonitorsGoldLCP" {
  bucket = aws_s3_bucket.gasMonitorsGold.id

  rule {
    id = "rule-1"

    filter {
      prefix = ""
    }

    transition {
      days = 180
      storage_class = "STANDARD_IA"
    }

    transition {
      days = 366
      storage_class = "GLACIER"
    }
    status = "Enabled"
  }
}

locals {
  target_buckets = {
    bronze = aws_s3_bucket.gasMonitorsBronze.id
    silver = aws_s3_bucket.gasMonitorsSilver.id
    gold   = aws_s3_bucket.gasMonitorsGold.id
  }
}

resource "aws_s3_bucket_public_access_block" "bucketAccessBlock" {
  for_each = local.target_buckets
  bucket = each.value

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}