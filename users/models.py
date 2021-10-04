from django.db import models
from django.contrib.auth.models import AbstractUser


class ExtendedUser(AbstractUser):
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    phone_number = models.CharField(max_length=16)
    
    def __str__(self):
        return self.username
