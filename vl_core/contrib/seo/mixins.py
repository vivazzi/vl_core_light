from django.db import models
from django.utils.translation import gettext as _


class SEOMixin(models.Model):
    meta_tags = models.CharField(
        _('Meta keywords'), max_length=255, blank=True,
        help_text=_('A list of tags (keywords) separated by commas.<br>'
                    'The recommended number of words is up to 10, the total number of characters is 150 characters.<br>'
                    'For example: personal growth trainings, improving memory, introducing good habits')
    )

    meta_desc = models.CharField(_('Meta description'), max_length=255, blank=True,
                                 help_text=_('A short description of the page. Recommended length is 120-160 characters.<br>'
                                             'For example: Personal growth trainings from specialists of the highest category'))

    class Meta:
        abstract = True
