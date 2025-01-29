import boto3
import os
from botocore.exceptions import NoCredentialsError
from models.file import File
from models import db_session
import logging
from sqlalchemy.exc import SQLAlchemyError


# Load environment variables for AWS credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize S3 client
s3_client = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=S3_REGION
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileResolver:
    @staticmethod
    def get_file(id):
        """Retrieve file metadata from PostgreSQL and generate a pre-signed S3 URL"""
        file = db_session.query(File).filter(File.id == id).first()
        if not file:
            return None  # File does not exist

        try:
            # Generate a pre-signed URL for secure file access
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': S3_BUCKET_NAME, 'Key': file.s3_key},
                ExpiresIn=3600  # URL expires in 1 hour
            )

            # Return a GraphQL FileType object instead of a dictionary
            return File(
                id=file.id,
                name=file.name,
                size=file.size,
                tags=file.tags,
                upload_date=file.upload_date,
                s3_key=file.s3_key,
                download_url=presigned_url  # Include the pre-signed URL
            )

        except NoCredentialsError:
            return {"error": "AWS credentials not configured properly"}
        
    @staticmethod
    def add_file(name, size, tags, s3_key):
        """Stores file metadata in the PostgreSQL database."""
        try:
            logger.info("\nAttempting to store file metadata: "
                        f"name={name}, size={size}, tags={tags}, s3_key={s3_key}")

            new_file = File(name=name, size=size, tags=tags, s3_key=s3_key)
            db_session.add(new_file)

            # Flush the session to detect integrity errors before commit
            db_session.flush()

            # Commit the transaction
            db_session.commit()

            logger.info(f"Metadata stored successfully for file: {name}")
            return new_file

        except SQLAlchemyError as e:
            db_session.rollback()  # Rollback the transaction on error
            logger.error(f"Error storing file metadata: {str(e)}")
            return None
