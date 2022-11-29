from abc import ABC, abstractmethod

from djangocms_text_ckeditor.models import Text

from vl_core.utils.core import humanize_bytes


class BaseSpeedUp(ABC):
    accelerated = False

    @abstractmethod
    def speed_up(self):
        return {}


class RemoveNbspFromTextPlugin(BaseSpeedUp):
    def speed_up(self):
        total = 0
        plugins = Text.objects.filter(body__icontains=' ')
        for plugin in plugins:
            total += plugin.body.count(' ')
            plugin.body = plugin.body.replace(' ', ' ')
            plugin.save()

        if total > 0:
            self.accelerated = True

        return {'free_bytes': humanize_bytes(total)}
