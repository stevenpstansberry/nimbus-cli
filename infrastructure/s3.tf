resource "aws_s3_bucket" "nimbus_cli_bucket" {
  bucket = "nimbus-cli-bucket"

  tags = {
    Name        = "Nimbus CLI Bucket"
    Environment = "dev"
  }
}

# Separate resource for server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "nimbus_cli_bucket_encryption" {
  bucket = aws_s3_bucket.nimbus_cli_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Separate resource for versioning
resource "aws_s3_bucket_versioning" "nimbus_cli_bucket_versioning" {
  bucket = aws_s3_bucket.nimbus_cli_bucket.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Separate resource for lifecycle rules
resource "aws_s3_bucket_lifecycle_configuration" "nimbus_cli_bucket_lifecycle" {
  bucket = aws_s3_bucket.nimbus_cli_bucket.id

  rule {
    id     = "transition-to-glacier"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
