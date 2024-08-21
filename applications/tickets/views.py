from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.http import Http404
from applications.core.models import Event
from .helpers import TicketWithQRCodeSender
from .serializers import TicketSerializer, TicketPurchaseSerializer
from .permissions import IsOwner
from .models import Ticket


class TicketCheckerAPIView(APIView):
    serializer_class = TicketSerializer
    permission_classes = (
        IsAuthenticated,
        IsOwner,
    )

    def get_object(self, event_id, ticket_id):
        try:
            return Ticket.objects.get(
                id=ticket_id, template__event=event_id, is_used=False, is_sold=True
            )
        except Exception as exc:
            raise Http404 from exc

    def get(self, request, event_id, ticket_id):
        """
        This route checks if received event_id and ticket_id are valid
        and belongs ticket to this event.
        If it's so, then marks a ticket as used, otherwise returns an error
        """
        obj = self.get_object(event_id, ticket_id)
        obj.is_used = True
        obj.save()
        serializer = self.serializer_class(instance=obj)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TicketAPIView(APIView):
    serializer_class = TicketPurchaseSerializer
    permission_classes = (AllowAny,)

    def get_object(self, event_id):
        """
        Get first available ticket that belongs to the chosen event
        """
        return Ticket.objects.filter(template__event=event_id, is_sold=False).first()

    def post(self, request, event_id):
        """
        This route returns available ticket by sending it to retrieved email address.
        Actually this should checking if user paid for a ticket, but this version
        of the application has no payment system implemented yet, this is why
        it returns the ticket immediately
        """
        data = request.data
        if request.user.is_authenticated:
            # assign email address if is authenticated
            data["email"] = request.user.email

        # Check if event_id is valid (exists and isn't free)
        if Event.objects.filter(id=event_id, is_free=False).exists():
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                obj = self.get_object(event_id)
                if not obj:
                    raise Http404

                assert isinstance(serializer.data, dict)
                # Generate PDF and send to provided email address
                TicketWithQRCodeSender.generate_and_send(serializer.data["email"], obj)
                obj.is_sold = True
                obj.save()
                return Response(
                    {
                        "Message": """
                            The ticket was sent to the provided email address.
                            You should be able to see it in a moment
                        """,
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors)
        raise Http404
