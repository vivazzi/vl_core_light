from django.apps import AppConfig
from django.db.models.signals import post_delete
from django.utils.translation import gettext_lazy as _

from vl_core.contrib.media_utils.mixins import FileModelMixin


def remove_folder(sender, instance, **kwargs):
    for field in instance.get_file_fields():
        instance.remove_folder(field)


class MediaUtilsConfig(AppConfig):
    name = 'vl_core.contrib.media_utils'
    verbose_name = _('VL Media Utils')

    def ready(self):
        from django.apps import apps

        for model in apps.get_models():
            if issubclass(model, FileModelMixin):
                post_delete.connect(remove_folder, sender=model)
