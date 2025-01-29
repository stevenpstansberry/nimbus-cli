import graphene
from models.file_type import FileType
from resolvers.file_resolver import FileResolver


# Define the Query
class Query(graphene.ObjectType):
    getFile = graphene.Field(FileType, id=graphene.Int(required=True))

    def resolve_getFile(self, info, id):
        file_data = FileResolver.get_file(id)
        if not file_data:
            return None
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
