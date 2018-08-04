import collections

from oscarapi.views.root import PUBLIC_APIS
from oscarapi.views.root import PROTECTED_APIS
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

__all__ = ('api_root',)


def PUBLIC_SUPPORT_APIS(r, f):
    return [
        ('tickets', reverse('ticket-list', request=r, format=f)),
        ('add-ticket', reverse('ticket-add-ticket', request=r, format=f)),
        # ('update-ticket', reverse('ticket-update-ticket', request=r, format=f)),
    ]


def PROTECTED_SUPPORT_APIS(r, f):
    return []


@api_view(('GET',))
def api_root(request, format=None):
    """
    GET:
    Display all available urls.
    Since some urls have specific permissions, you might not be able to access
    them all.
    """
    apis = PUBLIC_APIS(request, format)
    apis += PUBLIC_SUPPORT_APIS(request, format)
    if request.user.is_staff:
        apis += PROTECTED_APIS(request, format)
        apis += PROTECTED_SUPPORT_APIS(request, format)

    return Response(collections.OrderedDict(apis))
