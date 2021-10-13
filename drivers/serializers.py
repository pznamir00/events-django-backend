from rest_framework import serializers
from .helpers import get_auth_data_by_driver_name
from .models import Platform


class PlatformSerializer(serializers.ModelSerializer):
    auth_fields = serializers.SerializerMethodField('get_auth_fields')
    
    class Meta:
        model = Platform
        fields = '__all__'
        
    def get_auth_fields(self, obj):
        """
        This method returns the auth fields from Driver class
        that row is related with. That fields are required during
        creating new UserPlatformRelation object.  

        Args:
            obj (Platform) : ---

        Returns:
            tuple: fields that are required by driver class as input
        """
        return get_auth_data_by_driver_name(driver_name=obj.driver_class_name)