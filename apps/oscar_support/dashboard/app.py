from django.conf.urls import url
from django.contrib.admin.views.decorators import staff_member_required

from shortuuid import get_alphabet

from oscar.core.application import DashboardApplication

from . import views


class SupportDashboardApplication(DashboardApplication):
    name = 'support-dashboard'
    default_permissions = ['is_staff', ]

    ticket_list_view = views.TicketListView
    ticket_create_view = views.TicketCreateView
    ticket_update_view = views.TicketUpdateView
    types_edit_view = views.TypesEditView
    statuses_edit_view = views.StatusesEditView
    priorities_edit_view = views.PrioritiesEditView

    def get_urls(self):
        urls = [
            url(r'^ticket/$', self.ticket_list_view.as_view(), name='ticket-list'),
            url(r'^ticket/create/$', self.ticket_create_view.as_view(),
                name='ticket-create'),
            url(
                r'^ticket/update/(?P<pk>[{0}]+)/$'.format(get_alphabet()),
                self.ticket_update_view.as_view(),
                name='ticket-update'
            ),
            url(
                r'tags/types/$', self.types_edit_view.as_view(),
                name='tag-type-list'
            ),
            url(
                r'tags/statuses/$', self.statuses_edit_view.as_view(),
                name='tag-status-list'
            ),
            url(
                r'tags/priorities/$', self.priorities_edit_view.as_view(),
                name='tag-priority-list'
            ),
        ]
        return self.post_process_urls(urls)


application = SupportDashboardApplication()
