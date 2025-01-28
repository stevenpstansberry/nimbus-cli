#!/usr/bin/env python

import click

@click.group()
def cli():
    """Nimbus CLI - Manage datasets in the cloud."""
    pass

@cli.command()
@click.argument('file_path')
def upload(file_path):
    """Upload a file to the cloud."""
    print(f"Simulated upload: {file_path}")

@cli.command()
def hello():
    print("hello")

if __name__ == "__main__":
    cli()
