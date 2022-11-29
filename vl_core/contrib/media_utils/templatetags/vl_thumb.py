from django import template

from vl_core.contrib.media_utils.thumb import thumb_data, thumb_html

register = template.Library()


@register.simple_tag(name='thumb_data')
def do_thumb_data(field, width=None, height=None):
    return thumb_data(field, width, height)


@register.simple_tag
def thumb(field, width=None, height=None, coordinates=None, th_type='cover', tag='img', silent=False):
    return thumb_html(field, width, height, coordinates, th_type, tag, silent)
