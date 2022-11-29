from xml.etree import cElementTree

from django.core.exceptions import ValidationError
from django.db.models import URLField
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.forms import ImageField as DjangoImageField
from django.core.validators import FileExtensionValidator, get_available_image_extensions

from vl_core.contrib.media_utils.files.images import SvgImageFile
from vl_core.contrib.media_utils.utils import upload_to_handler
from vl_core.contrib.media_utils.widgets import PicURLWidget, FileWidget, PicWidget


class PicURLField(URLField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255
        self.w = kwargs.pop('w', None)
        self.h = kwargs.pop('h', None)
        self.th_type = kwargs.pop('th_type', 'cover')
        self.use_fb = kwargs.pop('use_fb', True)
        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = PicURLWidget(w=self.w, h=self.h, th_type=self.th_type, use_fb=self.use_fb)
        return super().formfield(**kwargs)


class FileField(models.FileField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255

        if 'upload_to' not in kwargs:
            kwargs['upload_to'] = upload_to_handler

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = FileWidget
        return super().formfield(**kwargs)

    # workaround for allauth
    # fixme: may be there is case to remove it
    def from_db_value(self, value, expression, connection):
        return value


class SvgImageFieldFile(SvgImageFile, ImageFieldFile):
    pass


def validate_svg(f):
    # Find "start" word in file and get "tag" from there
    f.seek(0)
    tag = None
    try:
        for event, el in cElementTree.iterparse(f, ('start',)):
            tag = el.tag
            break
    except cElementTree.ParseError:
        pass

    # Check that this "tag" is correct
    if tag != '{http://www.w3.org/2000/svg}svg':
        raise ValidationError('Uploaded file is not an image or SVG file.')

    # Do not forget to "reset" file
    f.seek(0)

    return f


def validate_image_file_extension(value):
    default_extensions = get_available_image_extensions()
    default_extensions.append('svg')
    return FileExtensionValidator(allowed_extensions=default_extensions)(value)


class SVGAndImageFormField(DjangoImageField):
    default_validators = [validate_image_file_extension]

    def to_python(self, data):
        try:
            f = super().to_python(data)
        except ValidationError:
            return validate_svg(data)

        return f


class PicField(FileField, models.ImageField):
    attr_class = SvgImageFieldFile

    def __init__(self, *args, **kwargs):

        self.use_fb = kwargs.pop('use_fb', True)
        self.th_type = kwargs.pop('th_type', 'contain')
        self.w = kwargs.pop('w', None)
        self.h = kwargs.pop('h', None)

        super().__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs['widget'] = PicWidget(attname=self.attname, w=self.w, h=self.h, th_type=self.th_type, use_fb=self.use_fb)
        kwargs['form_class'] = SVGAndImageFormField

        return models.ImageField.formfield(self, **kwargs)
