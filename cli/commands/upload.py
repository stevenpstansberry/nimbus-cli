import boto3
import os
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables from .env
load_dotenv()

# Retrieve the S3 bucket name from the .env file
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_path, object_key=None, tags=None):
    """
    Uploads a file to the predefined S3 bucket and optionally adds tags.

    Args:
        file_path (str): Local path to the file to upload.
        object_key (str, optional): Key for the file in S3. Defaults to the file name.
        tags (dict, optional): A dictionary of tags to apply to the S3 object.

    Returns:
        str: URL of the uploaded file in S3.
    """
    if not BUCKET_NAME:
        print("Error: S3 bucket name not configured. Check your .env file.")
        return None

    # Set the object key to the file name if not provided
    if object_key is None:
        object_key = os.path.basename(file_path)

    # Initialize the S3 client
    s3_client = boto3.client('s3')

    try:
        # Upload the file
        s3_client.upload_file(file_path, BUCKET_NAME, object_key)

        # If tags are provided, apply them to the object
        if tags:
            tag_set = [{"Key": k, "Value": v} for k, v in tags.items()]
            s3_client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=object_key,
                Tagging={"TagSet": tag_set}
            )

        # Generate the file URL
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"
        return file_url

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}.")
        return None
    except NoCredentialsError:
        print("Error: AWS credentials not configured.")
        return None
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials configuration.")
        return None
