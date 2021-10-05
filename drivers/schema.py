import graphene
import json
from .models import Platform
from graphene_django import DjangoObjectType





class PlatformType(DjangoObjectType):
    auth_data_format = graphene.String()

    class Meta:
        model = Platform
        fields = ('id', 'name', 'description', 'url', )

    @staticmethod
    def resolve_auth_data_format(root, info, **kwargs):
        class_name = root.driver_class_name
        driver_module = __import__(f"drivers.drivers.{class_name}", fromlist=[class_name])
        _class = getattr(driver_module, class_name)
        auth_fields = _class.get_required_fields()        
        return json.dumps(auth_fields)
    
    



class Query(graphene.ObjectType):
    all_platforms = graphene.List(PlatformType)
    
    def resolve_all_platforms(root, info):
        return Platform.objects.all()