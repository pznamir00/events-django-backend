from django.db import models


class Platform(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    driver_class_name = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_created=True)
    
    def __str__(self):
        return self.name