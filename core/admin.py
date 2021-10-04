from django.contrib import admin
from .models import UserPlatformChoice, ItemOffer, Item

admin.site.register(UserPlatformChoice)
admin.site.register(Item)
admin.site.register(ItemOffer)
