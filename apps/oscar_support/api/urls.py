import django
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    # url(r'^', include(router.urls, namespace='support-api')),
    url(r'^$', views.api_root, name='support-api'),
    url(r'^tickets/$', views.TicketList.as_view(), name='ticket-list'),
    url(r'^tickets/(?P<pk>[a-zA-Z0-9]+)/$', views.TicketDetail.as_view(), name='ticket-detail'),
    url(r'^ticket/add-ticket/$', views.AddTicketView.as_view(), name='ticket-add-ticket'),
    # url(r'^ticket/update-ticket/$', views.UpdateTicketView.as_view(), name='ticket-update-ticket'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

if django.VERSION[:2] < (1, 8):
    from django.conf.urls import patterns

    urlpatterns = patterns('', *urlpatterns)
