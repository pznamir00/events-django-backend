from datetime import datetime
from unittest.mock import MagicMock, patch
import pytest
from applications.core.choices import Category
from applications.core.models import Event
from mixer.backend.django import mixer
from applications.core.serializers import (
    EventDetailSerializer,
    EventSimpleSerializer,
    FollowedHashTagSerializer,
)
from django.core.files.uploadedfile import SimpleUploadedFile


class TestFollowedHashTagSerializer:
    def test_validation_passes_if_data_is_correct(self):
        instance = FollowedHashTagSerializer(data={"value": "New hashtag"})
        assert instance.is_valid()

    def test_validation_does_not_pass_if_value_is_missing(self):
        instance = FollowedHashTagSerializer(data={})
        assert not instance.is_valid()

    @pytest.mark.django_db
    def test_returns_data_in_correct_format(self):
        hashtag = mixer.blend("core.FollowedHashTag")
        hashtag.value = "new value"  # type: ignore
        instance = FollowedHashTagSerializer(instance=hashtag)
        assert instance.data == {"value": "new value"}


class TestEventSimpleSerializer:
    def test_validation_passes_if_data_is_correct(self):
        instance = EventSimpleSerializer(data=get_event_detail_data())
        assert instance.is_valid()

    def test_validation_does_not_pass_if_data_is_invalid(self):
        instance = EventSimpleSerializer(
            data={
                "title": "new event",
                "category": Category.CONCERT,
                "is_free": True,
            }
        )
        assert not instance.is_valid()

    @pytest.mark.django_db
    def test_returns_data_in_correct_format(self):
        event = mixer.blend("core.Event")
        instance = EventSimpleSerializer(instance=event)
        assert "title" in instance.data
        assert "location" in instance.data
        assert "event_datetime" in instance.data
        assert "category" in instance.data
        assert "is_free" in instance.data


class TestEventDetailSerializer:
    def test_validation_passes_if_data_is_correct(self):
        instance = EventDetailSerializer(data=get_event_detail_data())
        assert instance.is_valid()

    def test_validation_does_not_pass_if_data_is_missing(self):
        data = get_event_detail_data()
        del data["title"]
        instance = EventDetailSerializer(data=data)
        assert not instance.is_valid()

    def test_validation_does_not_pass_if_is_not_free_but_ticket_is_missing(self):
        data = {**get_event_detail_data(), "is_free": False}
        instance = EventDetailSerializer(data=data)
        assert not instance.is_valid()

    def test_validation_passes_if_is_not_free_and_ticket_is_provided(self):
        data = {
            **get_event_detail_data(),
            "is_free": False,
            "ticket": {
                "file": SimpleUploadedFile("test_file.pdf", b"file_content"),
                "quantity": 10,
            },
        }
        instance = EventDetailSerializer(data=data)
        assert instance.is_valid()

    def test_validation_does_not_pass_if_ticket_is_invalid(self):
        data = {
            **get_event_detail_data(),
            "is_free": False,
            "ticket": {
                "file": SimpleUploadedFile("test_file.pdf", b"file_content"),
            },
        }
        instance = EventDetailSerializer(data=data)
        assert not instance.is_valid()

    @pytest.mark.django_db
    @patch(
        "applications.core.serializers.EventDetailSerializer.ticket_generator_service"
    )
    def test_create_calls_generate_tickets_if_should(self, mock: MagicMock):
        instance = EventDetailSerializer(data=get_event_detail_data())
        instance.is_valid()
        instance.save()
        mock.generate_if_needed.assert_called_once()

    @pytest.mark.django_db
    @patch(
        "applications.core.serializers.EventDetailSerializer.ticket_generator_service"
    )
    def test_update_calls_generate_tickets_if_should(self, mock: MagicMock):
        event: Event = mixer.blend("core.Event")
        instance = EventDetailSerializer(instance=event, data=get_event_detail_data())
        instance.is_valid()
        instance.save()
        mock.generate_if_needed.assert_called_once()


def get_event_detail_data():
    return {
        "title": "new event",
        "description": "this is new event",
        "location": {"latitude": 3.14, "longitude": 21.37},
        "event_datetime": datetime(2020, 10, 10, 10, 10, 10),
        "category": Category.CONCERT,
        "is_free": True,
    }
