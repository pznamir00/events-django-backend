import graphene
from .models import Platform
from graphene_django import DjangoObjectType


class PlatformType(DjangoObjectType):
    class Meta:
        model = Platform
        fields = ('id', 'name', 'description', 'url')
        

class Query(graphene.ObjectType):
    all_platforms = graphene.List(PlatformType)
    
    def resolve_all_platforms(self, info):
        return Platform.objects.all()