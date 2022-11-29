from urllib.parse import parse_qs, urlencode, urlsplit

from django import template

register = template.Library()


@register.simple_tag
def add_to_query_string(url, **kwargs):
    qs = parse_qs(urlsplit(url).query)
    qs.update(**kwargs)
    return f'{urlsplit(url).path}?{urlencode(qs)}'


@register.simple_tag
def remove_from_query_string(url, *args):
    qs = parse_qs(urlsplit(url).query)
    for arg in args:
        if arg in qs:
            del qs[arg]

    return f'{urlsplit(url).path}?{urlencode(qs)}'
