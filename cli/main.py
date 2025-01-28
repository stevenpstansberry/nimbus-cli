#!/usr/bin/env python

import click
from commands.upload import upload_file_to_s3 

@click.group()
def cli():
    """Nimbus CLI - Manage datasets in the cloud."""
    pass

@cli.command()
@click.argument('file_path')
@click.option('--key', required=False, help="The S3 object key. Defaults to the file name.")
def upload(file_path, key):
    """
    Upload a file to the cloud.

    Args:
        file_path (str): Path to the local file.
        key (str, optional): The S3 object key.
    """
    print(f"Uploading {file_path} to the S3 bucket...")
    file_url = upload_file_to_s3(file_path, key)
    if file_url:
        print(f"File successfully uploaded to {file_url}")
    else:
        print("File upload failed.")

@cli.command()
def hello():
    print("hello")

if __name__ == "__main__":
    cli()
