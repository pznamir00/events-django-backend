from rest_framework.views import APIView
from rest_framework.response import Response
from core.models import Event
from .serializers import TicketSerializer
from rest_framework.permissions import AllowAny
from .models import Ticket
from django.http import Http404
from .helpers import TicketWithQRCodeSender

class TicketAPIView(APIView):
    serializer_class = TicketSerializer
    permission_classes = (AllowAny,)
    
    def get_object(self, event_id):
        """
        Get first available ticket that belongs to the choosed event
        """
        return Ticket.objects.filter(template__event=event_id).first()

    def get(self, request, event_id=None):
        print(event_id)
    
    def post(self, request, event_id):
        """
        This route returns available ticket by sending it to retrived email address.
        Actually this should checking if user paid for a ticket, but this version
        of the application has no payment system implemented yet, this is why 
        it returns the ticket immediately
        """
        data = request.data
        if request.user.is_authenticated:
            """
            assign email address if is authenticated
            """
            data['email'] = request.user.email
        
        """
        Check if event_id is valid (exists and isn't free)
        """
        if Event.objects.filter(id=event_id, is_free=False).exists():
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                obj = self.get_object(event_id)
                if not obj:
                    return Http404
                
                """
                Generate PDF and send to provided email address
                """
                TicketWithQRCodeSender.generate_and_send(serializer.data['email'], obj)
                obj.sold = True
                obj.save()
                return Response({
                    'Message': 'The ticket was sent to the provided email address. You should be able to see it in a moment',
                    'data': serializer.data
                })
            return Response(serializer.errors)
        return Http404