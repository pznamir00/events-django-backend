from datetime import datetime, timedelta
from typing import cast
import pytest
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from applications.core.choices import Category
from applications.core.models import Event, FollowedHashTag
from applications.core.tests.utils import errors_to_dict
from applications.core.views import (
    EventOwnListViewSet,
    EventViewSet,
    FollowedHashTagView,
)
from applications.users.models import User
from mixer.backend.django import mixer
from django.contrib.gis.geos import Point


@pytest.mark.django_db
class TestFollowedHashTagView:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", email="test@gmail.com"
        )
        self.client = APIClient()
        self.view = FollowedHashTagView.as_view(
            {"get": "list", "post": "create", "delete": "destroy"}
        )

    def test_view_throws_an_401_if_user_is_not_auth(self):
        request = APIRequestFactory().get("")
        response = self.view(request)
        assert response.status_code == 401

    def test_get_returns_only_tags_that_belong_to_user(self):
        request = APIRequestFactory().get("")
        other_user = User.objects.create_user(username="other", password="123passWord")
        mixer.blend("core.FollowedHashTag", user=other_user, value="hashtag1")
        mixer.blend("core.FollowedHashTag", user=other_user, value="hashtag2")
        mixer.blend("core.FollowedHashTag", user=self.user, value="hashtag3")
        mixer.blend("core.FollowedHashTag", user=self.user, value="hashtag4")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["value"] == "hashtag3"
        assert response.data[1]["value"] == "hashtag4"

    def test_post_throws_error_if_value_is_missing(self):
        request = APIRequestFactory().post("", {})
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 400
        assert errors_to_dict(response.data) == {"value": ["This field is required."]}

    def test_post_saves_new_hashtag_with_slugified_value(self):
        request = APIRequestFactory().post("", {"value": "New Hashtag"})
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 201
        hashtag = FollowedHashTag.objects.latest("pk")
        assert hashtag.user == self.user
        assert hashtag.value == "newhashtag"

    def test_delete_destroys_object(self):
        hashtag: FollowedHashTag = mixer.blend(
            "core.FollowedHashTag", user=self.user, value="hashtag"
        )
        request = APIRequestFactory().delete("")
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=hashtag.pk)
        assert response.status_code == 204
        remains = FollowedHashTag.objects.filter(pk=hashtag.pk).exists()
        assert not remains


@pytest.mark.django_db
class TestEventOwnListViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", email="test@gmail.com"
        )
        self.client = APIClient()
        self.view = EventOwnListViewSet.as_view({"get": "list"})

    def test_view_throws_an_401_if_user_is_not_auth(self):
        request = APIRequestFactory().get("")
        response = self.view(request)
        assert response.status_code == 401

    def test_get_returns_only_tags_that_belong_to_user(self):
        request = APIRequestFactory().get("")
        other_user = User.objects.create_user(username="other", password="123passWord")
        mixer.blend("core.Event", promoter=other_user, title="event1")
        mixer.blend("core.Event", promoter=other_user, title="event2")
        mixer.blend("core.Event", promoter=self.user, title="event3")
        mixer.blend("core.Event", promoter=self.user, title="event4")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]["title"] == "event3"
        assert response.data[1]["title"] == "event4"


@pytest.mark.django_db
class TestEventViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user = User.objects.create_user(
            username="testuser", password="password", email="test@gmail.com"
        )
        self.client = APIClient()
        self.view = EventViewSet.as_view(
            {"get": "list", "post": "create", "delete": "destroy", "put": "update"}
        )

    def test_get_returns_only_publicly_available_events(self):
        request = APIRequestFactory().get("")
        mixer.blend("core.Event", title="event1", is_private=True)
        mixer.blend("core.Event", title="event2", canceled=True)
        mixer.blend("core.Event", title="event3", took_place=True)
        mixer.blend("core.Event", title="event4")
        force_authenticate(request, user=self.user)
        response = self.view(request)
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["title"] == "event4"

    def test_get_returns_events_sorted_by_distance(self):
        request = APIRequestFactory().get(
            "",
            data={
                "latitude": "3",
                "longitude": "3",
                "ordering": "distance",
            },
        )
        create_event("event1", Point(10, 15))
        create_event("event2", Point(9, 3))
        create_event("event3", Point(50, 78))
        response = self.view(request)
        assert response.data[0]["title"] == "event2"
        assert response.data[1]["title"] == "event1"
        assert response.data[2]["title"] == "event3"

    def test_get_returns_filtered_events(self):
        request = APIRequestFactory().get(
            "",
            data={
                "latitude": "3",
                "longitude": "3",
                "keywords": "ppp",
                "range": "1000",
                "is_free": False,
            },
        )
        create_event("event1", Point(10, 15), 1)
        create_event("event2", Point(9, 3), 1)
        create_event("event3-ppp", Point(50, 78), 1, is_free=False)
        create_event("event4", Point(50, 78), 1)
        create_event("event5", Point(50, 78), 1)
        create_event("event6-ppp", Point(4, 5), 1, is_free=False)
        create_event("event7-ppp", Point(8, 9), 1)
        response = self.view(request)
        assert len(response.data) == 1
        assert response.data[0]["title"] == "event6-ppp"

    def test_get_throws_error_if_range_filter_is_missing_lat_or_lon(self):
        request = APIRequestFactory().get(
            "",
            data={
                "latitude": "3",
                "keywords": "ppp",
                "range": "1000",
                "is_free": False,
            },
        )
        response = self.view(request)
        assert response.status_code == 400

    def test_get_single_returns_details(self):
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().get("")
        response = EventViewSet.as_view({"get": "retrieve"})(request, pk=event.id)
        assert "title" in response.data
        assert "histories" in response.data
        assert "location" in response.data
        assert "location_hints" in response.data
        assert "image" in response.data

    def test_post_throws_error_if_user_is_not_authenticated(self):
        request = APIRequestFactory().post(
            "",
            data={"title": "new event", "description": "some description"},
        )
        response = self.view(request)
        assert response.status_code == 401

    def test_post_throws_error_if_data_is_invalid(self):
        request = APIRequestFactory().post(
            "",
            data={"title": "new event", "description": "some description"},
        )
        force_authenticate(request, self.user)
        response = self.view(request)
        assert response.status_code == 400
        assert errors_to_dict(response.data) == {
            "location": ["This field is required."],
            "event_datetime": ["This field is required."],
            "category": ["This field is required."],
        }

    def test_post_creates_new_event(self):
        data = get_event_payload()
        request = APIRequestFactory().post("", data=data, format="json")
        force_authenticate(request, self.user)
        response = self.view(request)
        assert response.status_code == 201
        obj = Event.objects.latest("pk")
        assert obj.title == "new event"

    def test_delete_throws_error_if_user_is_not_auth(self):
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().delete("")
        response = self.view(request, pk=event.id)
        assert response.status_code == 401

    def test_delete_throws_error_if_user_is_not_owner(self):
        other_user = User.objects.create_user(username="other", password="123passWord")
        event = create_event("event 1", Point(1, 1), 1, promoter=other_user)
        request = APIRequestFactory().delete("")
        force_authenticate(request, self.user)
        response = self.view(request, pk=event.id)
        assert response.status_code == 403

    def test_delete_destroys_event_if_user_is_owner(self):
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().delete("")
        force_authenticate(request, self.user)
        response = self.view(request, pk=event.id)
        assert response.status_code == 204
        assert not Event.objects.filter(id=event.id).exists()

    def test_delete_destroys_event_if_user_is_superuser(self):
        superuser = create_superuser()
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().delete("")
        force_authenticate(request, superuser)
        response = self.view(request, pk=event.id)
        assert response.status_code == 204
        assert not Event.objects.filter(id=event.id).exists()

    def test_put_throws_error_if_user_is_not_auth(self):
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().put("", {})
        response = self.view(request, pk=event.id)
        assert response.status_code == 401

    def test_put_throws_error_if_user_is_not_owner(self):
        other_user = User.objects.create_user(username="other", password="123passWord")
        event = create_event("event 1", Point(1, 1), 1, promoter=other_user)
        request = APIRequestFactory().put("", {})
        force_authenticate(request, self.user)
        response = self.view(request, pk=event.id)
        assert response.status_code == 403

    def test_put_throws_error_if_payload_is_invalid(self):
        data = get_event_payload()
        del data["title"]
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().put("", data, format="json")
        force_authenticate(request, self.user)
        response = self.view(request, pk=event.id)
        assert response.status_code == 400

    def test_put_updates_event_if_user_is_owner(self):
        data = {**get_event_payload(), "title": "new title"}
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().put("", data, format="json")
        force_authenticate(request, self.user)
        response = self.view(request, pk=event.id)
        assert response.status_code == 200
        obj = Event.objects.get(id=event.id)
        assert obj.title == "new title"

    def test_put_updates_event_if_user_is_superuser(self):
        superuser = create_superuser()
        data = {**get_event_payload(), "title": "new title"}
        event = create_event("event 1", Point(1, 1), 1, promoter=self.user)
        request = APIRequestFactory().put("", data, format="json")
        force_authenticate(request, superuser)
        response = self.view(request, pk=event.id)
        assert response.status_code == 200
        obj = Event.objects.get(id=event.id)
        assert obj.title == "new title"


def create_event(title: str, location: Point, in_days=0, **kwargs):
    return cast(
        Event,
        mixer.blend(
            "core.Event",
            title=title,
            location=location,
            event_datetime=datetime.now() + timedelta(days=in_days),
            **kwargs,
        ),
    )


def get_event_payload():
    return {
        "title": "new event",
        "description": "some description",
        "location": {"latitude": 13, "longitude": 33.89},
        "event_datetime": datetime(2020, 10, 10),
        "category": Category.MOVIE_FESTIVAL,
    }


def create_superuser():
    return User.objects.create_superuser(
        username="other", password="123passWord", email="super@gmail.com"
    )
