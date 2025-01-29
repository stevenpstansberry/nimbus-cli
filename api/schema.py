import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from models.file import File
from resolvers.file_resolver import FileResolver

# Define the FileType for GraphQL
class FileType(SQLAlchemyObjectType):
    class Meta:
        model = File

# Define the Query
class Query(graphene.ObjectType):
    list_files = graphene.List(FileType)

    def resolve_list_files(self, info):
        return FileResolver.list_files()

# Define the Mutation
class AddFile(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        size = graphene.Int(required=True)
        tags = graphene.String(required=False)
        s3_key = graphene.String(required=True)

    file = graphene.Field(lambda: FileType)

    def mutate(self, info, name, size, tags, s3_key):
        file = FileResolver.add_file(name, size, tags, s3_key)
        return AddFile(file=file)

class Mutation(graphene.ObjectType):
    add_file = AddFile.Field()

# Combine Query and Mutation into the Schema
schema = graphene.Schema(query=Query, mutation=Mutation)
