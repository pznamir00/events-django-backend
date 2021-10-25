from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

  

class User(AbstractUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    phone_number = PhoneNumberField(null=True, default="")
    
    def __str__(self):
        return self.email
