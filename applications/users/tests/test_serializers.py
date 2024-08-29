import pytest
from mixer.backend.django import mixer
from applications.users.models import User
from applications.users.serializers import ExtendedRegisterSerializer, UserSerializer


class TestExtendedRegisterSerializer:
    @pytest.mark.django_db
    def test_passes_if_data_is_valid(self):
        data = {
            "username": "piklop",
            "password1": "111qrtp9b3d5",
            "password2": "111qrtp9b3d5",
            "email": "test@gmail.com",
            "phone_number": "499038195",
            "country": "USA",
            "state": "Virginia",
            "city": "city",
            "street": "street",
            "home_nb": "3",
            "zip_code": "1234",
        }
        instance = ExtendedRegisterSerializer(data=data)
        assert instance.is_valid()

    @pytest.mark.django_db
    def test_throws_error_if_fields_are_missing(self):
        data = {
            "username": "piklop",
            "password1": "111qrtp9b3d5",
            "email": "test@gmail.com",
            "phone_number": "499038195",
            "state": "Virginia",
            "city": "city",
            "street": "street",
            "home_nb": "3",
            "zip_code": "1234",
        }
        instance = ExtendedRegisterSerializer(data=data)
        assert not instance.is_valid()

    @pytest.mark.django_db
    def test_throws_error_if_passwords_do_not_match(self):
        data = {
            "username": "piklop",
            "password1": "111qrtp9b3d5",
            "password2": "efre532",
            "email": "test@gmail.com",
            "phone_number": "499038195",
            "country": "USA",
            "state": "Virginia",
            "city": "city",
            "street": "street",
            "home_nb": "3",
            "zip_code": "1234",
        }
        instance = ExtendedRegisterSerializer(data=data)
        assert not instance.is_valid()


class TestUserSerializer:
    @pytest.mark.django_db
    def test_returns_object(self):
        user: User = mixer.blend("users.User")
        instance = UserSerializer(instance=user)
        assert "email" in instance.data
        assert "phone_number" in instance.data
        assert "is_superuser" in instance.data
        assert "country" in instance.data
        assert "state" in instance.data
        assert "city" in instance.data
        assert "street" in instance.data
        assert "home_nb" in instance.data
        assert "zip_code" in instance.data
        assert "avatar" in instance.data
