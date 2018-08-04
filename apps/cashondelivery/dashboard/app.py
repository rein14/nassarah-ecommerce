import django
from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from oscar.core.application import Application

from . import views


class CashOnDeliveryDashboardApplication(Application):
    name = None
    default_permissions = ['is_staff', ]

    list_view = views.TransactionListView
    detail_view = views.TransactionDetailView

    def get_urls(self):
        urlpatterns = [
            url(r'^transactions/$', self.list_view.as_view(),
                name='cashondelivery-transaction-list'),
            url(r'^transactions/(?P<pk>\d+)/$', self.detail_view.as_view(),
                name='cashondelivery-transaction-detail'),
        ]

        if django.VERSION[:2] < (1, 8):
            from django.conf.urls import patterns

            urlpatterns = patterns('', *urlpatterns)

        return self.post_process_urls(urlpatterns)


application = CashOnDeliveryDashboardApplication()
