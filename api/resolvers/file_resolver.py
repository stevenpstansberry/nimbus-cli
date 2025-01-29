import boto3
import os
from botocore.exceptions import NoCredentialsError
from models.file import File
from models.file_type import FileType
from models import db_session
import logging
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()


# Load environment variables for AWS credentials
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
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

# Check if bucket name exists
if not BUCKET_NAME:
    logging.error("Error: S3_BUCKET_NAME is not set. Check your .env file!")

class FileResolver:
    @staticmethod
    def get_file(id):
        """Retrieve file metadata from PostgreSQL and generate a pre-signed S3 URL"""
        # Set session to autocommit mode for read-only queries
        db_session.autocommit = True

        file = db_session.query(File).filter(File.id == id).first()
        
        if not file:
            logger.warning(f"File with ID {id} not found in database.")
            return None  # File does not exist

        try:
            # Debugging logs
            logger.info(f"Retrieved file metadata from DB: id={file.id}, name={file.name}, s3_key={file.s3_key}")
            logger.info(f"S3_BUCKET_NAME={BUCKET_NAME}")

            # Ensure `s3_key` is not None
            if not file.s3_key:
                logger.error(f"Error: File ID {id} does not have a valid s3_key in the database.")
                return None

            if not BUCKET_NAME:
                logger.error("Error: S3_BUCKET_NAME is not set. Check your environment variables.")
                return None

            # Generate a pre-signed URL for secure file access
            presigned_url = s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': BUCKET_NAME, 'Key': file.s3_key},
                ExpiresIn=3600  # URL expires in 1 hour
            )

            logger.info(f"Generated pre-signed URL: {presigned_url}")

            # Return a GraphQL FileType object
            return FileType(
                id=file.id,
                name=file.name,
                size=file.size,
                tags=file.tags,
                upload_date=file.upload_date,
                s3_key=file.s3_key,
                download_url=presigned_url  
            )

        except NoCredentialsError:
            logger.error("AWS credentials not configured properly.")
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
