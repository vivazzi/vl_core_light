from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db.models import DurationField as BaseDurationField, CharField
from django.forms import Select, HiddenInput
from django.utils.translation import gettext as _

from vl_core.template_pool import template_pool
from vl_core.widgets import ColorPickerWidget, DeltaTimeDurationWidget


class TemplateField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        super(TemplateField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        if not hasattr(self.model, 'pool'):
            self.model.pool = self.model.__name__

        templates = template_pool.templates[self.model.pool] if self.model.pool in template_pool.templates else {}
        if not templates:
            kwargs['widget'] = HiddenInput()
        else:
            choices = []
            if self.blank is True:
                choices.append(('', '---------'))

            choices.extend([(name, template.title) for name, template in templates.items()])

            kwargs['widget'] = Select(choices=choices)
        return super(TemplateField, self).formfield(**kwargs)


class ColorField(CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 30
        self.use_opacity = kwargs.pop('use_opacity', True)
        super(ColorField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = ColorPickerWidget(use_opacity=self.use_opacity)
        return super(ColorField, self).formfield(**kwargs)


def validate_timedelta(value):
    if not isinstance(value, timedelta):
        raise ValidationError(_('A valid time period is required'))


class DeltaTimeDurationField(BaseDurationField):
    default_validators = [validate_timedelta, ]

    def formfield(self, **kwargs):
        kwargs['widget'] = DeltaTimeDurationWidget
        return super().formfield(**kwargs)
