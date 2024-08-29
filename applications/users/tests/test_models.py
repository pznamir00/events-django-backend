import pytest
from mixer.backend.django import mixer
from applications.users.models import User


@pytest.mark.django_db
class TestUser:
    def test_create_user(self):
        entity = mixer.blend("users.User")
        assert isinstance(entity, User), "Should create a User instance"  # type: ignore
