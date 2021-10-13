from drivers.helpers import get_auth_data_by_driver_name
from rest_framework.serializers import ValidationError
from drivers.models import Platform
import json


class PlatformAuthDataValidator:
    def __call__(self, value):
        platform_id = value['platform']
        driver_name = Platform.objects.filter(id=platform_id).values('driver_name')
        auth_data = get_auth_data_by_driver_name(driver_name=driver_name)
        for field in auth_data:
            if field not in value:
                raise ValidationError(f'Data that you passed is missing field: {field}')