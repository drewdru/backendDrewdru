import graphene
import api.schema

class Query(api.schema.TaskQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(api.schema.TaskMutations, graphene.ObjectType):
  	pass

schema = graphene.Schema(query=Query, mutation=Mutation)
