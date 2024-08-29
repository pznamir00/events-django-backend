from django.urls import reverse, resolve
import pytest
from applications.users import views


@pytest.mark.urls("applications.users.urls")
class TestUsersUrls:
    def test_user_url_resolves(self):
        url = reverse("user")
        assert resolve(url).func.view_class == views.UserAPIView  # type: ignore
