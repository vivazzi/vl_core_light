from os.path import splitext

from django import template
from django.contrib.staticfiles.storage import staticfiles_storage
from sass_processor.processor import sass_processor

from vl_core.contrib.admin_utils.conf import app_settings

register = template.Library()


@register.simple_tag
def theming_url():
    url = app_settings.ADMIN_TOOLS_THEMING_CSS
    if splitext(url)[1] == '.scss':
        url = sass_processor(url)

    return url


@register.simple_tag
def admin_favicon_url():
    return  staticfiles_storage.url(app_settings.ADMIN_FAVICON_URL)
