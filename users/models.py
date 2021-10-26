from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

  

class User(AbstractUser):
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    phone_number = PhoneNumberField(null=True, default="")
    country = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    street = models.CharField(max_length=128)
    home_nb = models.CharField(max_length=16)
    zip_code = models.CharField(max_length=16)
    
    def __str__(self):
        return self.email
