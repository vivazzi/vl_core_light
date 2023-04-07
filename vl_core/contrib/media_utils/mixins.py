import shutil
from os import listdir, remove
from os.path import exists, dirname, join, basename

from django.conf import settings
from django.core.exceptions import SuspiciousFileOperation
from django.utils.functional import classproperty
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from vl_core.contrib.media_utils.fields import FileField, PicField
from vl_core.contrib.media_utils.templatetags.vl_thumb import thumb as get_thumb
from vl_core.contrib.media_utils.widgets import PicWidget
from vl_core.utils.os import is_file_changed


class FileModelMixin:
    def file_field_names(self):
        return [field.name for field in self._meta.fields if isinstance(field, FileField)]

    file_field_names = property(file_field_names)

    def upload_to(cls):
        app = cls._meta.app_label
        res = []
        for i, char in enumerate(cls._meta.object_name):
            if i != 0 and char.isupper():
                res.append('_')
            res.append(char)
        upload_to = ''.join(res).lower()
        if upload_to[-1] == 'y': return '{}_{}ies'.format(app, upload_to[:-1])
        elif upload_to[-1] in ('s', 'x', 'h'): return '{}_{}es'.format(app, upload_to)
        else: return '{}_{}s'.format(app, upload_to)

    upload_to = classproperty(upload_to)

    def main_file_field_name(self):
        return self.file_field_names[0]

    main_file_field_name = property(main_file_field_name)

    def get_main_field(self):
        return getattr(self, self.main_file_field_name)

    def get_field(self, field_name=''):
        if not field_name: return self.get_main_field()
        else: return getattr(self, field_name)

    def get_file_fields(self):
        return [getattr(self, f) for f in self.file_field_names]

    def file_exists(self, field_name='', field=None):
        if not field:
            field = self.get_field(field_name)

        try:
            return bool(field) and exists(field.path)
        except SuspiciousFileOperation:
            return False

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id:
            try:
                old_obj = self.__class__.objects.get(id=self.id)

                for i, old_file in enumerate(old_obj.get_file_fields()):
                    new_file = getattr(self, self.file_field_names[i])
                    if is_file_changed(old_file, new_file): self.remove_folder(old_file)

            except self.__class__.DoesNotExist:
                pass

        super().save(force_insert, force_update, using, update_fields)

    def remove_folder(self, field=''):
        if self.file_exists(field=field):
            file_dir = dirname(field.path)
            checked_upload_to_dir = dirname(file_dir)

            # check upload_to_dirs to avoid wrong deletion
            if checked_upload_to_dir == join(settings.MEDIA_ROOT, self.upload_to) and exists(file_dir):
                shutil.rmtree(file_dir)

    class Meta:
        abstract = True


class PicModelMixin(FileModelMixin):
    thumb_size = (135, 100)

    def get_pic_field(self, field_name=''):
        if not field_name:
            for field in self._meta.fields:
                if isinstance(field, PicField):
                    field_name = field.attname
                    break

        return getattr(self, field_name)

    def thumb(self, field_name=''):
        field = self.get_pic_field(field_name)
        return mark_safe(get_thumb(field, self.thumb_size[0], self.thumb_size[1]))
    thumb.short_description = _('Thumbnail')

    def fb_pic(self, field_name=''):
        field = self.get_pic_field(field_name)
        return PicWidget(field.field.attname, use_input=False, use_resize_orig_image=False).render(field.field.attname, field)
    fb_pic.short_description = _('Image')

    def remove_all_thumbs(self):
        for field_name in self.file_field_names:
            self.remove_thumbs(field_name)

    def remove_thumbs(self, field_name=''):
        if self.file_exists(field_name):
            field = self.get_field(field_name)
            if issubclass(field.field, PicField):
                folder = dirname(field.path)
                for f in listdir(folder):
                    if f != basename(field.name): remove(join(folder, f))


class FBThumbMediaMixin:
    class Media:
        css = {'all': ['vl_media_utils/th.css', 'vl_media_utils/contrib/fancybox/fancybox.css', 'vl_media_utils/fb_wr.css']}


# def _copy_relations_handler(obj, old_instance):
#     obj.folder = generate_folder(os.path.join(settings.MEDIA_ROOT, obj.upload_to), 5)
#
#     for i, old_file in enumerate(old_instance.get_files()):
#         file_field = obj.file_fields[i]
#         if bool(old_file):
#             f_postfix = file_field if len(old_instance.get_files()) >= 2 else ''
#             setattr(obj, file_field, copy_file_changing_folder(old_file, obj.folder, f_postfix))
#             change_folder(old_file.path)
#
#     obj.save()
#     [change_folder(f.path, reverse=True) for f in old_instance.get_files() if bool(f)]
#
#
# def copy_relations_fk(self, old_instance, fk, related_name_for_files='pics'):
#     for obj in getattr(old_instance, related_name_for_files).all():
#         old_obj = copy(obj)
#         obj.id = None
#         setattr(obj, fk, self)
#         _copy_relations_handler(obj, old_obj)
