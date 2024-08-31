import pytest
from mixer.backend.django import mixer
from applications.core.models import Event, EventHistory, FollowedHashTag
from applications.users.models import User


@pytest.mark.django_db
class TestEvent:
    def test_create_event(self):
        entity = mixer.blend("core.Event")
        assert isinstance(entity, Event), "Should create a Event instance"


@pytest.mark.django_db
class TestEventHistory:
    def test_create_event_history(self):
        entity = mixer.blend("core.EventHistory")
        assert isinstance(entity, EventHistory), "Should create a EventHistory instance"


@pytest.mark.django_db
class TestFollowedHashTag:
    def test_create_followed_hashtag(self):
        entity = mixer.blend("core.FollowedHashTag")
        assert isinstance(
            entity, FollowedHashTag
        ), "Should create a FollowedHashTag instance"
