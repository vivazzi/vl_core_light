from datetime import timedelta

from django.conf import settings
from django.forms import TextInput, Media, MultiWidget, NumberInput
from django.template.loader import render_to_string
from django.utils.dateparse import parse_duration
from django.utils.translation import gettext as _

from django_select2.forms import Select2Widget as BaseSelect2Widget

from sass_processor.processor import sass_processor


# noinspection PyProtectedMember
class Select2Widget(BaseSelect2Widget):
    """
    Added jquery to widget
    """
    def _get_media(self):
        media = super()._get_media()

        extra = '' if settings.DEBUG else '.min'
        js = [f'admin/js/vendor/jquery/jquery{extra}.js', 'admin/js/jquery.init.js', 'vl_core/admin_compat.js']
        js.extend(media._js)

        return Media(js=js, css={'screen': media._css['screen']})

    media = property(_get_media)


class ColorPickerWidget(TextInput):
    def __init__(self, attrs=None, use_opacity=True):
        super().__init__(attrs)

        self.use_opacity = use_opacity

    class Media:
        css = {'all': [sass_processor('vl_core/widgets/color_picker/color_picker.scss'), ]}
        extra = '' if settings.DEBUG else '.min'
        js = [f'admin/js/vendor/jquery/jquery{extra}.js', 'admin/js/jquery.init.js', 'vl_core/admin_compat.js',
              'vl_core/widgets/color_picker/color_picker.js']

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        context = {'name': name,
                   'color': value or '#000',
                   'old_color': value,
                   'use_opacity': self.use_opacity,
                   'input_html': input_html}
        return render_to_string('vl_core/widgets/color_picker.html', context)


class DeltaTimeDurationWidget(MultiWidget):
    template_name = 'vl_core/widgets/delta_time_duration.html'

    def __init__(self, attrs=None):
        widgets = (NumberInput(), NumberInput(), NumberInput(), NumberInput())
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            duration = parse_duration(value)

            m, sec = divmod(duration.total_seconds(), 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)

            return [int(d), int(h), int(m), sec]
        return [None, None, None, None]

    def get_context(self, name, value, attrs):
        ctx = super().get_context(name, value, attrs)

        labels = (_('d'), _('h'), _('m'), _('sec'))
        for i, widget in enumerate(ctx['widget']['subwidgets']):
            widget['label'] = labels[i]

        return ctx

    def value_from_datadict(self, data, files, name):
        values = [float(widget.value_from_datadict(data, files, f'{name}_{i}') or 0) for i, widget in enumerate(self.widgets)]
        if not any(values):
            return None

        try:
            return timedelta(days=values[0], hours=values[1], minutes=values[2], seconds=values[3])
        except ValueError:
            return None

    class Media:
        css = {'all': ['vl_core/widgets/duration/duration.css', ]}
