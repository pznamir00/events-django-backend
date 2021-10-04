import graphene
from users.schema import AuthMutation, Query as AuthQuery
from drivers.schema import Query as DriverQuery
from .models import UserPlatformChoice, Item, ItemOffer




class Mutation(AuthMutation, graphene.ObjectType):
    pass

class Query(AuthQuery, DriverQuery, graphene.ObjectType):
    pass




schema = graphene.Schema(query=Query, mutation=Mutation)