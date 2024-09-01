from typing import TYPE_CHECKING, Any, List, Optional, Tuple
import uuid
from django.template.defaultfilters import slugify
from rest_framework.request import Request
from applications.core.choices import HistoryLabel
from applications.tickets.helpers import TicketGenerator

if TYPE_CHECKING:
    from applications.core.models import Event


class EventService:
    def register_event_history_base_on_changes(self, event: "Event", changes: dict):
        from applications.core.models import (  # pylint:disable=import-outside-toplevel
            EventHistory,
        )

        known_action = False
        histories: List[EventHistory] = []

        if changes.get("event_datetime"):
            # Changed event datetime
            histories.append(
                EventHistory(
                    event=event,
                    label=HistoryLabel.MOVED,
                    text=f"{event.event_datetime} ===> {changes.get('event_datetime')}",
                )
            )
            known_action = True

        if changes.get("took_place"):
            # The event took place
            histories.append(EventHistory(event=event, label=HistoryLabel.TOOK_PLACE))
            known_action = True

        if changes.get("canceled"):
            # Canceled an event
            histories.append(EventHistory(event=event, label=HistoryLabel.CANCELED))
            known_action = True

        if not known_action:
            # Note update
            histories.append(
                EventHistory(event=event, label=HistoryLabel.DETAILS_CHANGED)
            )

        if histories:
            EventHistory.objects.bulk_create(histories)


class TicketGeneratorService:
    def generate_if_needed(self, data: dict, ticket_data: dict, event: "Event"):
        ticket_generator = TicketGenerator(data)
        if ticket_generator.should_generate_tickets():
            ticket_generator.generate_tickets(ticket_data, event)


class SlugService:
    def create_slug(self, value: str):
        return slugify(value).replace("-", "")


class EventFileNameGeneratorService:
    @staticmethod
    def generate(_: Any, filename: str):
        extension = filename.split(".")[-1]
        return f"media/events/{uuid.uuid4()}.{extension}"


class FilterService:
    def get_lat_lon_from_query_params(
        self, request: Request
    ) -> Optional[Tuple[float, float]]:
        try:
            lat = request.query_params.get("latitude", "")
            lon = request.query_params.get("longitude", "")
            lat = float(lat)
            lon = float(lon)
            return (lat, lon)
        except ValueError:
            return None
