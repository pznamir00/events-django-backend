from django.db import models
from users.models import ExtendedUser
from drivers.models import Platform


class UserPlatformChoice(models.Model):
    user = models.ForeignKey(ExtendedUser, on_delete=models.CASCADE, related_name='platforms')
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)


class Item(models.Model):
    name = models.CharField(max_length=128)
    short_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_created=True)
    
    def __str__(self):
        return self.name
    
    
class ItemOffer(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    platform = models.ForeignKey(UserPlatformChoice, on_delete=models.SET_NULL, null=True)
    url = models.URLField(max_length=1024)
    
    def __str__(self):
        return self.item.name + ' -> ' + self.platform.driver.name + ' Offer'