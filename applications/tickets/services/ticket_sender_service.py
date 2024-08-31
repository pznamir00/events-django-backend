import os
import io
import time
import qrcode
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.core.files import File
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from applications.tickets.models import Ticket


class TicketSenderService:
    """
    This class is up to sending ticket file to client's email address.
    It generates unique QR code (based on id of ticket), and pdf file
    (based on selected template file). Then it merges this 2 files saved
    in media/tmp with unique names, and sends the result to provided email
    address.
    """

    def send(self, email: str, ticket: Ticket):
        # get pdf file from template
        pdf = ticket.template.file  # pylint: disable=protected-access
        # generate qr code and get path to it
        qr_path = self.__make_qr(ticket)
        # generate new pdf (ticket) and get path to it
        pdf_path = self.__make_pdf(qr_path, pdf)
        # send files
        self.__send(email, pdf_path, qr_path)
        # delete files from tmp
        self.__delete_files(pdf_path, qr_path)

    def __make_qr(self, ticket: Ticket):
        """
        This method generates qr code and saves it in media/tmp directory.
        For this purpose it uses a qrcode lib.
        """
        # get domain
        current_site = Site.objects.get_current()
        domain = current_site.domain
        # prepare link to validate ticket
        path = f"{domain}/api/tickets/check/{ticket.id}/"
        # generate qr code
        img = qrcode.make(path)
        # save code as .png in media/tmp
        name = f"media/tmp/{time.time() * 1000}.png"
        img.save(name)
        return name

    def __make_pdf(self, qr_path: str, pdf: File):
        """
        This method generates a PDF file (actually a ticket that client'll receive)
        """
        # path to file
        pdf_path = f"media/tmp/{(time.time() * 1000)}.pdf"
        packet = io.BytesIO()
        # create canvas with qr code
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawImage(qr_path, 0, 0, 250, 250)
        can.save()
        # create pdf file
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(pdf)
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        with open(pdf_path, "wb") as content:
            output.write(content)
        return pdf_path

    def __send(self, recipient_email: str, pdf_path: str, qr_path: str):
        email = EmailMessage(
            "Hello, Events here",
            "You are getting your own ticket below",
            "events@gmail.com",
            [recipient_email],
        )
        email.attach_file(pdf_path)
        email.attach_file(qr_path)
        return email.send()

    def __delete_files(self, file_path: str, qr_path: str):
        os.remove(file_path)
        os.remove(qr_path)
