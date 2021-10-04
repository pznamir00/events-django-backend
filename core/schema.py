import graphene
from users.schema import AuthMutation, Query as AuthQuery




class Mutation(AuthMutation, graphene.ObjectType):
    pass

class Query(AuthQuery, graphene.ObjectType):
    pass




schema = graphene.Schema(query=Query, mutation=Mutation)