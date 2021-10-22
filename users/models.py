from django.db import models
from django.contrib.auth.models import AbstractUser
from address.models import AddressField
from phonenumber_field.modelfields import PhoneNumberField

  

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField('Email address', unique=True)
    phone_number = PhoneNumberField()
    address = AddressField()
    REQUIRED_FIELDS = ['']
    
    def __str__(self):
        return self.email
