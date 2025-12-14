resource "aws_dynamodb_table" "bronzerMetadata" {
  name           = "bronzeMetadata"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Bucket"
  range_key      = "Object"

  attribute {
    name = "Bucket"
    type = "S"
  }

  attribute {
    name = "Object"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

  tags = {
    Product = "metadata"
  }
}

resource "aws_dynamodb_table" "silverMetadata" {
  name           = "silverMetadata"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Bucket"
  range_key      = "Object"

  attribute {
    name = "Bucket"
    type = "S"
  }

  attribute {
    name = "Object"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

  tags = {
    Product = "metadata"
  }
}

resource "aws_dynamodb_table" "goldMetadata" {
  name           = "goldMetadata"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "Bucket"
  range_key      = "Object"

  attribute {
    name = "Bucket"
    type = "S"
  }

  attribute {
    name = "Object"
    type = "S"
  }

  ttl {
    attribute_name = "TimeToExist"
    enabled        = true
  }

  tags = {
    Product = "metadata"
  }
}