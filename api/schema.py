import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.file import File
from resolvers.file_resolver import FileResolver

# Define the FileType for GraphQL
class FileType(SQLAlchemyObjectType):
    class Meta:
        model = File

    download_url = graphene.String()  # Add pre-signed URL field

# Define the Query
class Query(graphene.ObjectType):
    get_file = graphene.Field(FileType, id=graphene.Int(required=True))

    def resolve_get_file(self, info, id):
        file_data = FileResolver.get_file(id)
        if not file_data:
            return None  # File not found
        return file_data

# Define the Mutation to Add File Metadata
class AddFile(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        size = graphene.Int(required=True)
        tags = graphene.String(required=False)
        s3_key = graphene.String(required=True)

    success = graphene.Boolean()

    def mutate(self, info, name, size, tags, s3_key):
        file = FileResolver.add_file(name, size, tags, s3_key)
        return AddFile(success=True if file else False)


# Create a Mutation Class
class Mutation(graphene.ObjectType):
    add_file = AddFile.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
