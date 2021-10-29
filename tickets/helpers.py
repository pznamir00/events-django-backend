from .models import Ticket, TicketTemplate
from django.contrib.sites.models import Site
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import letter
from django.core.mail import EmailMessage
import qrcode
import os
import io
import time





class TicketGenerator:
    """
    This class generates tickets with provided quantity by user
    if it is necessery (that means when user provided 'is_free' field
    and is set on False). User has to pass template file and quantity
    of tickets to generate and in this point generates them.
    """
    def generate_if_provided(data, ticket, event):
        if 'is_free' in data and not data['is_free']:
            # save a template
            template = TicketTemplate.objects.create(event=event, template=ticket['template'])
            for i in range(ticket['quantity']):
                # creating single tickets
                Ticket.objects.create(template=template)
                




class TicketWithQRCodeSender:
    """
    This class is up to sending ticket file to client's email address.
    It generates unique QR code (based on id of ticket), and pdf file 
    (based on selected template file). Then it merges this 2 files saved
    in media/tmp with unique names, and send the outcome to provided email
    address.
    """
    def generate_and_send(email, obj):
        #get pdf file from template
        pdf = obj.template._file
        #generate qr code and get path to it
        qr_path = TicketWithQRCodeSender.make_qr(obj)
        #generate new pdf (ticket) and get path to it
        pdf_path = TicketWithQRCodeSender.make_pdf(qr_path, pdf)
        #send files
        TicketWithQRCodeSender.send(email, pdf_path, qr_path)
        #delete files from tmp
        TicketWithQRCodeSender.delete_files(pdf_path, qr_path)
        return True

    def make_qr(obj):
        """
        This method generates qr code and saves it in media/tmp directory.
        For this purpose it uses a qrcode lib.
        """
        #get domain
        current_site = Site.objects.get_current()
        domain = current_site.domain
        #prepare link to validate ticket
        path = f'{domain}/api/tickets/check/{obj.id}/'
        #generate qr code
        img = qrcode.make(path)
        #save code as .png in media/tmp
        name = 'media/tmp/' + str(time.time() * 1000) + '.png'
        img.save(name)
        return name

    def make_pdf(qr_path, pdf):
        """
        This method generates a PDF file (actually a ticket that client'll receive)
        """
        #path to file
        pdf_path = 'media/tmp/' + str(time.time() * 1000) + '.pdf'
        packet = io.BytesIO()
        #create canvas with qr code
        can = canvas.Canvas(packet, pagesize=letter)
        can.drawImage(qr_path, 0, 0, 250, 250)
        can.save()
        #create pdf file
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        existing_pdf = PdfFileReader(pdf)
        output = PdfFileWriter()
        page = existing_pdf.getPage(0)
        page.mergePage(new_pdf.getPage(0))
        output.addPage(page)
        outputStream = open(pdf_path, "wb")
        output.write(outputStream)
        outputStream.close()
        return pdf_path

    def send(recipient_email, pdf_path, qr_path):
        email = EmailMessage(
            'Hello, Events here',
            'You are getting your own ticket below',
            'events@gmail.com',
            [recipient_email]
        )
        email.attach_file(pdf_path)
        email.attach_file(qr_path)
        return email.send()

    def delete_files(file_path, qr_path):
        os.remove(file_path)
        os.remove(qr_path)

