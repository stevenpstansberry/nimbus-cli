resource "aws_db_instance" "nimbus_db" {
  identifier              = "nimbus-postgres-db"
  engine                  = "postgres"
  instance_class          = "db.t3.micro"
  allocated_storage       = 20
  max_allocated_storage   = 100
  db_name                    = "nimbusdb"
  username                = var.db_username
  password                = var.db_password
  publicly_accessible     = false
  skip_final_snapshot     = true

  tags = {
    Name        = "Nimbus DB"
    Environment = "dev"
  }
}
