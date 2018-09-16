from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class DashboardConfig(AppConfig):
    label = 'mobilemoney_dashboard'
    name = 'mobilemoney.dashboard'
    verbose_name = _('Mobile Money Dashboard')
