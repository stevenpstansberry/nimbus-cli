import boto3
import os
import requests
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables
load_dotenv()

# Retrieve the S3 bucket name and GraphQL API URL from .env file
BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
GRAPHQL_URL = os.getenv("GRAPHQL_URL", "http://localhost:5000/graphql")

def upload_file_to_s3(file_path, object_key=None, tags=None):
    """
    Uploads a file to the predefined S3 bucket and stores metadata in PostgreSQL via GraphQL.

    Args:
        file_path (str): Local path to the file to upload.
        object_key (str, optional): Key for the file in S3. Defaults to the file name.
        tags (dict, optional): A dictionary of tags to apply to the S3 object.

    Returns:
        str: URL of the uploaded file in S3 if successful, else None.
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
        # Get file size
        file_size = os.path.getsize(file_path)

        # Upload the file to S3
        s3_client.upload_file(file_path, BUCKET_NAME, object_key)

        # Apply tags if provided
        if tags:
            tag_set = [{"Key": k, "Value": v} for k, v in tags.items()]
            s3_client.put_object_tagging(
                Bucket=BUCKET_NAME,
                Key=object_key,
                Tagging={"TagSet": tag_set}
            )

        # Generate the file URL
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{object_key}"

        # Convert tags dictionary to a string for GraphQL
        tags_str = ",".join([f"{k}:{v}" for k, v in tags.items()]) if tags else ""

        # Send metadata to GraphQL API
        graphql_response = send_metadata_to_graphql(
            name=os.path.basename(file_path),
            size=file_size,
            tags=tags_str,
            s3_key=object_key
        )

        if graphql_response:
            print(f"File successfully uploaded and metadata stored: {file_url}")
            return file_url
        else:
            print("File upload succeeded, but metadata storage failed.")
            return None

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}.")
        return None
    except NoCredentialsError:
        print("Error: AWS credentials not configured.")
        return None
    except PartialCredentialsError:
        print("Error: Incomplete AWS credentials configuration.")
        return None

def send_metadata_to_graphql(name, size, tags, s3_key):
    """
    Sends file metadata to the GraphQL API for storage in PostgreSQL.

    Args:
        name (str): File name.
        size (int): File size in bytes.
        tags (str): Comma-separated tags.
        s3_key (str): The file's S3 key (path in S3).

    Returns:
        bool: True if the request was successful, False otherwise.
    """
    mutation = """
    mutation($name: String!, $size: Int!, $tags: String!, $s3Key: String!) {
        addFile(name: $name, size: $size, tags: $tags, s3Key: $s3Key) {
            success  # ✅ Remove "file" and only return success
        }
    }
    """
    
    variables = {
        "name": name,
        "size": size,
        "tags": tags if tags else "",  # Ensure tags is a string
        "s3Key": s3_key,
    }
    
    response = requests.post(GRAPHQL_URL, json={"query": mutation, "variables": variables})

    response_data = response.json()
    print("GraphQL Response:", response_data)  # Debugging output

    if response.status_code == 200 and response_data.get("data", {}).get("addFile", {}).get("success"):
        return True
    else:
        print("Error storing metadata:", response_data)
        return False

