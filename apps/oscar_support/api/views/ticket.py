from rest_framework import generics

from oscar.core.loading import get_model
from oscar_support.api import serializers  # permissions

__all__ = (
    'TicketList',
    'TicketDetail',
    'AddTicketView',
)

Ticket = get_model('oscar_support', 'Ticket')


class TicketList(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketLinkSerializer


class TicketDetail(generics.RetrieveAPIView):
    queryset = Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class AddTicketView(generics.ListCreateAPIView):
    """
    Create a new ticket.
    POST(ticket, attachment,
         [total, shipping_method_code, shipping_charge, billing_address]):
    {
        "type": "Products",
        "subject": "Title for ticket",
        "requester": "@username",
        "body": "Text for ticket",
        "attachments": [
            {
                "uuid": "znup8iQM2rWmg7r8RiNCGd",
                "user": "http://localhost:8000/api/users/#/",
                "date_created": "2017-10-05T21:44:59.361697Z",
                "date_updated": "2017-10-05T21:44:59.383862Z",
                "file": "http://localhost:8000/media/oscar_support/2017/10/PSI_Docker_Certification_Exam_lX6nNfE.pdf",
                "ticket": "rVszTeuXWcZ9fspMkYh7wd"
            },
            {
                "uuid": "Q8DNTzTXqtMXEDyfyeZFuY",
                "user": "http://localhost:8000/api/users/#/",
                "date_created": "2017-10-05T20:21:08.748900Z",
                "date_updated": "2017-10-05T21:44:59.339411Z",
                "file": "http://localhost:8000/media/oscar_support/2017/10/Invoice_Docker_Certification_lvnH4mk.pdf",
                "ticket": "rVszTeuXWcZ9fspMkYh7wd"
            }
        ]
    }
    returns the order object.
    """
    queryset = Ticket.objects.all()
    serializer_class = serializers.AddTicketSerializer

# class UpdateTicketView(APIView):
