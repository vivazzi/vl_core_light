import json

from django import template
from django.contrib.sites.shortcuts import get_current_site

from vl_core.utils.url import with_domain, get_domain

register = template.Library()


@register.filter(name='format')
def do_format(v, obj):
    return v.format(obj)


@register.filter(name='dict')
def do_dict(obj):
    return dict(obj)


@register.filter(name='get')
def do_get(obj, key):
    return obj.get(key)


@register.filter
def to_json(obj):
    return json.dumps(obj)


# --- site tags ---
@register.simple_tag
def get_site_name():
    return get_current_site(None).name


@register.simple_tag(name='get_domain')
def do_get_domain(with_protocol=True, with_slash=False):
    return get_domain(with_protocol, with_slash)


@register.filter(name='with_domain')
def do_with_domain(url):
    return with_domain(url)
# --- end: site tags ---
