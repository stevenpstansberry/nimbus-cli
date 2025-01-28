"""
CLI Package for Nimbus
"""

# Package metadata
__version__ = "0.1.0"
__author__ = "Steven Stansberry"

from .main import cli

# Define what is exposed when using "from cli import *"
__all__ = ["cli"]
