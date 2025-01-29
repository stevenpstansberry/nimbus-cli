# Define the FileType for GraphQL
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType

from api.models.file import File


class FileType(SQLAlchemyObjectType):
    class Meta:
        model = File

    download_url = graphene.String()  # Add pre-signed URL field