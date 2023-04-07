from django import template
from django.contrib.staticfiles.storage import staticfiles_storage

from vl_core.contrib.admin_utils.conf import app_settings

register = template.Library()


@register.simple_tag
def theming_url():
    return staticfiles_storage.url(app_settings.ADMIN_TOOLS_THEMING_CSS)


@register.simple_tag
def admin_favicon_url():
    return staticfiles_storage.url(app_settings.ADMIN_FAVICON_URL)
