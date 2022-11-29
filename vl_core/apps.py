from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules
from django.utils.translation import gettext_lazy as _


class VLCoreConfig(AppConfig):
    name = 'vl_core'
    verbose_name = _('VL Core')

    def ready(self):
        autodiscover_modules('vl_templates')
