from io import BytesIO
from os.path import exists

from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import Media, URLInput, CheckboxInput, TextInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from file_resubmit.widgets import ResubmitImageWidget, ResubmitFileWidget

from vl_core.contrib.media_utils.conf import app_settings
from vl_core.contrib.media_utils.thumb import thumb_from_field
from vl_core.contrib.media_utils.utils import default_compress_settings


class FileWidget(ResubmitFileWidget):
    pass


class PicMixin:
    open_original = True

    def get_thumb(self, value, w, h):
        return value, w, h

    def get_orig_url(self, value):
        return value

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        text_input_html = ''
        if getattr(self, 'use_input', True):
            text_input_html = super().render(name, value, attrs, renderer, **kwargs)

        pic_html = ''
        if value and not isinstance(value, InMemoryUploadedFile):
            url, width, height = self.get_thumb(value, self.w, self.h)
            ctx = {'url': url, 'name': name, 'width': width, 'height': height, 'th_type': self.th_type, 'open_original': self.open_original}

            if self.use_fb:
                ctx['orig_url'] = self.get_orig_url(value)

            if hasattr(value, 'path') and not exists(value.path):
                pic_html = render_to_string('vl_media_utils/no_img.html', ctx)
            else:
                pic_html = render_to_string(f'vl_media_utils/{"widgets/fb_wr" if self.use_fb else "adaptive_th_img"}.html', ctx)

        return mark_safe(render_to_string('vl_media_utils/widgets/pic_input.html', {'text_input_html': text_input_html, 'pic_html': pic_html}))

    def _get_media(self):
        css = ['vl_media_utils/th.css']

        if self.use_fb:
            css.extend(['vl_media_utils/contrib/fancybox/fancybox.css', 'vl_media_utils/fb_wr.css'])

        return Media(css={'screen': css})

    media = property(_get_media)


class ResizeOrigImageMixin:
    @property
    def use_optimize_name_field(self):
        return f'use_optimize_{self.attname}'

    def render(self, name, value, attrs=None, renderer=None, **kwargs):
        if not getattr(self, 'use_resize_orig_image', True):
            return super().render(name, value, attrs, renderer, **kwargs)

        text_input_html = super().render(name, value, attrs, renderer, **kwargs)

        checked = app_settings.PIC_FIELD_OPTIMIZE_PARS['checked_by_default']
        compress_field_html = CheckboxInput().render(self.use_optimize_name_field, None,
                                                     {'checked': checked, 'id': 'id_use_optimize'})

        if app_settings.USE_HINT_FOR_COMPRESSION:
            help_text = _('The original image will be reduced to {} pixels by width and {} pixels by height. Image quality: {}%<br/>'
                          'This function is only applicable when saving a newly loaded image.<br/>'
                          'Compression is not used for vector format files.').format(
                app_settings.PIC_FIELD_OPTIMIZE_PARS["max_size"]["width"],
                app_settings.PIC_FIELD_OPTIMIZE_PARS["max_size"]["height"],
                app_settings.PIC_FIELD_OPTIMIZE_PARS["quality"]
            )
            help_text = f'<div class="help">{help_text}</div>'
        else:
            help_text = ''

        label_text = _('Use image compression?')

        compress_field_html = (
            '<div style="margin-top:20px;margin-bottom:20px;">'
            f'{compress_field_html} <label class="vCheckboxLabel" for="id_use_optimize">{label_text}</label>'
            f'{help_text}'
            '</div>'
        )

        return mark_safe(''.join([text_input_html, compress_field_html]))

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name)
        if value:
            use_optimize = CheckboxInput().value_from_datadict(data, files, self.use_optimize_name_field)
            if use_optimize:
                name, ext = value.name.rsplit('.', 1)
                if ext != 'svg':
                    with Image.open(value) as new_pic:
                        new_pic.thumbnail(
                            (app_settings.PIC_FIELD_OPTIMIZE_PARS['max_size']['width'],
                             app_settings.PIC_FIELD_OPTIMIZE_PARS['max_size']['height']),
                            resample=Image.ANTIALIAS,
                        )
                        pic_file = BytesIO()
                        new_pic.save(pic_file, **default_compress_settings(new_pic))

                        pic_file.seek(0)
                        value = InMemoryUploadedFile(pic_file, getattr(value, 'field_name', None), f'{name}.jpg', 'image/jpeg',
                                                     pic_file.getbuffer().nbytes, None)

        return value


class PicWidget(ResizeOrigImageMixin, PicMixin, ResubmitImageWidget):
    def __init__(self, attname, attrs=None, w=None, h=None, th_type='contain', use_fb=True, use_resize_orig_image=True, use_input=True):
        super().__init__(attrs)

        if not w and not h:
            h = 150

        self.w = w
        self.h = h
        self.th_type = th_type
        self.attname = attname
        self.use_fb = use_fb
        self.use_resize_orig_image = use_resize_orig_image
        self.use_input = use_input

    def get_thumb(self, value, w, h):
        return thumb_from_field(value, w, h)

    def get_orig_url(self, value):
        return value.url


class PicURLWidget(PicMixin, URLInput):
    def __init__(self, attrs=None, w=None, h=None, th_type='cover', use_fb=True):
        super().__init__(attrs)
        self.w = w or 200
        self.h = h or 150
        self.th_type = th_type
        self.use_fb = use_fb


class ImageBase64Widget(PicMixin, TextInput):
    def __init__(self, attrs=None, w=None, h=None, th_type='cover', use_fb=True):
        super().__init__(attrs)

        if not w and not h:
            h = 150

        self.w = w
        self.h = h
        self.th_type = th_type
        self.use_fb = use_fb
        self.open_original = False
