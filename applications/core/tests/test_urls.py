from django.urls import reverse, resolve
import pytest
from applications.core import views


@pytest.mark.urls("applications.core.urls")
class TestCoreUrls:
    def test_followed_hashtags_url_resolves(self):
        url = reverse("followed-hashtags-list")
        assert resolve(url).func.cls == views.FollowedHashTagView  # type: ignore

    def test_events_url_resolves(self):
        url = reverse("events-list")
        assert resolve(url).func.cls == views.EventViewSet  # type: ignore

    def test_own_events_url_resolves(self):
        url = reverse("own-events-list")
        assert resolve(url).func.cls == views.EventOwnListViewSet  # type: ignore
