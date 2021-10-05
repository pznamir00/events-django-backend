import graphene
from users.schema import AuthMutation, Query as AuthQuery
from drivers.schema import Query as DriverQuery
from users.models import ExtendedUser
from .models import UserPlatformChoice, Item, ItemOffer
from graphene_django import DjangoObjectType



class CreateUserPlatformChoice(graphene.Mutation):
    class Arguments:
        platform = graphene.ID(required=True)
        auth_data = graphene.String(required=True)
        
    @staticmethod
    def mutate(root, info, **kwargs):
        print(info, kwargs)
        #user_platform_choice = UserPlatformChoice(
            #auth_data=auth_data,
            #platform=platform,
            #user=None
        #)
        #user_platform_choice.save()
        



class Mutation(AuthMutation, graphene.ObjectType):
    create_user_platform_choice = CreateUserPlatformChoice.Field()
    

class Query(AuthQuery, DriverQuery, graphene.ObjectType):
    pass




schema = graphene.Schema(query=Query, mutation=Mutation)