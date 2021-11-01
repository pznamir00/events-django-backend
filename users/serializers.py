from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User





class ExtendedRegisterSerializer(RegisterSerializer):
    def get_cleaned_data(self):
        super(ExtendedRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'password2': self.validated_data.get('password2', ''),
            'email': self.validated_data.get('email', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'country': self.validated_data.get('country', ''),
            'state': self.validated_data.get('state', ''),
            'city': self.validated_data.get('city', ''),
            'street': self.validated_data.get('street', ''),
            'home_nb': self.validated_data.get('home_nb', ''),
            'zip_code': self.validated_data.get('zip_code', ''),
        }





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email', 
            'phone_number', 
            'is_superuser', 
            'country',
            'state',
            'city',
            'street',
            'home_nb',
            'zip_code',
        )
        read_only_fields = ('email', 'is_superuser',)