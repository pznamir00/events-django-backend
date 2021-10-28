from .models import Ticket
from core.models import EventTemplate

class TicketGenerator:
    def generate_if_provided(data, ticket, event):
        if 'is_free' in data and not data['is_free']:
            # save a template
            template = EventTemplate.objects.create(
                event=event, 
                template=ticket['template']
            )
            for i in range(ticket['quantity']):
                # creating single tickets
                Ticket.objects.create(template=template)
                
class TicketWithQRCodeGenerator:
    def generate_and_send(email, obj):
        pass