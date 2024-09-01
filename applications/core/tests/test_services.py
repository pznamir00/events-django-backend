import datetime
from unittest.mock import patch, MagicMock

import pytest
from applications.core.choices import HistoryLabel
from applications.core.models import Event, EventHistory
from applications.core.services import (
    EventFileNameGeneratorService,
    EventService,
    FilterService,
    SlugService,
    TicketGeneratorService,
)
from mixer.backend.django import mixer


class TestEventFileNameGeneratorService:
    @patch("applications.core.services.uuid.uuid4", return_value="2137")
    def test_generate_makes_new_filename_from_provided(self, _: MagicMock):
        result = EventFileNameGeneratorService.generate(None, "example.png")
        assert result == "media/events/2137.png"


class TestSlugService:
    def test_create_slug_makes_slug_from_value(self):
        service = SlugService()
        slug = service.create_slug("Some Slug")
        assert slug == "someslug"


class TestTicketGeneratorService:
    def test_generate_if_needed_calls_generate_tickets_if_should(self):
        service = TicketGeneratorService()


class TestEventService:
    @pytest.mark.django_db
    def test_register_event_history_base_on_changes_creates_correct_histories(self):
        service = EventService()
        event: Event = mixer.blend("core.Event")
        changes = {"event_datetime": datetime.datetime(2020, 10, 10), "canceled": True}
        service.register_event_history_base_on_changes(event, changes)
        histories = EventHistory.objects.all()
        assert len(histories) == 2
        assert histories[0].label == HistoryLabel.MOVED
        assert histories[1].label == HistoryLabel.CANCELED

    @pytest.mark.django_db
    def test_register_event_history_base_on_changes_registers_generic_history_if_unknown(
        self,
    ):
        service = EventService()
        event: Event = mixer.blend("core.Event")
        changes = {}
        service.register_event_history_base_on_changes(event, changes)
        histories = EventHistory.objects.all()
        assert len(histories) == 1
        assert histories[0].label == HistoryLabel.DETAILS_CHANGED


class TestFilterService:
    def test_get_lat_lon_from_query_params_returns_lat_lon_if_defined(self):
        service = FilterService()
        req = MagicMock(query_params={"latitude": "3.14", "longitude": "12.99"})
        result = service.get_lat_lon_from_query_params(req)
        assert result == (3.14, 12.99)

    def test_get_lat_lon_from_query_params_returns_none_if_any_field_is_missing(self):
        service = FilterService()
        req = MagicMock(query_params={"latitude": "3.14"})
        result = service.get_lat_lon_from_query_params(req)
        assert not result
