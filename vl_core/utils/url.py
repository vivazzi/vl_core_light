from urllib.parse import urljoin

from django.contrib.sites.shortcuts import get_current_site

from vl_core.conf import app_settings


def get_domain(with_protocol=True, with_slash=False):
    protocol = f'{app_settings.PROTOCOL}://' if with_protocol else ''
    slash = '/' if with_slash else ''
    return f'{protocol}{get_current_site(None).domain}{slash}'


def with_domain(url):
    return urljoin(get_domain(), url)
