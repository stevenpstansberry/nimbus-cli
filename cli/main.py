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
@click.option('--tags', required=False, help="Comma-separated key:value pairs for tagging the file.")
def upload(file_path, key, tags):
    """
    Upload a file to the cloud with optional tags.

    Args:
        file_path (str): Path to the local file.
        key (str, optional): The S3 object key.
        tags (str, optional): Comma-separated key:value pairs for tagging the file.
    """
    # Parse tags into a dictionary
    tag_dict = {}
    if tags:
        try:
            tag_dict = dict(tag.split(":") for tag in tags.split(","))
        except ValueError:
            print("Error: Tags must be provided in the format key:value,key:value.")
            return

    print(f"Uploading {file_path} to the S3 bucket...")
    file_url = upload_file_to_s3(file_path, key, tags=tag_dict)
    if file_url:
        print(f"File successfully uploaded to {file_url}")
    else:
        print("File upload failed.")

@cli.command()
def hello():
    print("hello")

if __name__ == "__main__":
    cli()
