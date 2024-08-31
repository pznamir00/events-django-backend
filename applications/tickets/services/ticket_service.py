from applications.tickets.models import Ticket
from applications.tickets.services.ticket_sender_service import TicketSenderService


class TicketService:
    def mark_as_used(self, ticket: Ticket):
        ticket.is_used = True
        ticket.save()

    def mark_as_sold(self, ticket: Ticket):
        ticket.is_sold = True
        ticket.save()

    def checkout(self, email: str, ticket: Ticket):
        sender_service = TicketSenderService()
        sender_service.send(email, ticket)
        self.mark_as_sold(ticket)
