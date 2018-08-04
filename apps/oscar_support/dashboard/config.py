from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OscarSupportDashboardConfig(AppConfig):
    # label = 'support_dashboard'
    name = 'oscar_support.dashboard'
    verbose_name = _('Support dashboard')
