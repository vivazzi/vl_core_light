from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AdminUtilsConfig(AppConfig):
    name = 'vl_core.contrib.admin_utils'
    verbose_name = _('VL Admin Utils')
