output "s3_bucket_name" {
  value = aws_s3_bucket.nimbus_cli_bucket.bucket
}

output "iam_role_arn" {
  value = aws_iam_role.s3_access_role.arn
}

output "rds_endpoint" {
  value = aws_db_instance.nimbus_db.endpoint
}
