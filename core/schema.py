import graphene
from users.schema import AuthMutation, Query as AuthQuery
from drivers.schema import Query as DriverQuery
from .models import UserPlatformChoice
from users.models import ExtendedUser
from graphene_django import DjangoObjectType
from django_graphene_permissions.permissions import IsAuthenticated
from django_graphene_permissions import permissions_checker
from graphene_django_crud.types import DjangoCRUDObjectType, resolver_hints
from graphene_django.converter import convert_django_field
from django.db.models import JSONField
from graphene.types import generic




class UserPlatformChoiceCRUDType(DjangoCRUDObjectType):    
    class Meta:
        model = UserPlatformChoice
        fields = ('platform',)
        use_connection = False
        
    @permissions_checker([IsAuthenticated])
    def get_queryset(cls, info, **kwargs):
        return UserPlatformChoice(user=info.context.user)
    
    #@permissions_checker([IsAuthenticated])
    @classmethod
    def create(cls, parent, info, instance, data, *args, **kwargs):
        return super().create(parent, info, instance, data, *args, **kwargs)
    




class Mutation(AuthMutation, graphene.ObjectType):
    create_user_platform_choice = UserPlatformChoiceCRUDType.CreatedField()
    delete_user_platform_choice = UserPlatformChoiceCRUDType.DeletedField()
    
class Query(AuthQuery, DriverQuery, graphene.ObjectType):
    user_platform_choices = UserPlatformChoiceCRUDType.BatchReadField()

schema = graphene.Schema(query=Query, mutation=Mutation)