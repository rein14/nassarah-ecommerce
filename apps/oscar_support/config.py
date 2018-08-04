from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OscarSupportConfig(AppConfig):
    # label = 'support'
    name = 'oscar_support'
    verbose_name = _('Support')
