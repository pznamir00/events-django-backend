from applications.core.models import Event, FollowedHashTag
from applications.users.models import User


def get_user_hashtags(user: User):
    return FollowedHashTag.objects.filter(user=user)


def get_user_events(user: User):
    return Event.objects.filter(promoter=user)


def get_publicly_available_events():
    return Event.objects.filter(is_private=False, canceled=False, took_place=False)
