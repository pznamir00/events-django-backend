from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import related


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    def __str__(self):
        return 'Profile of ' + self.user.email
