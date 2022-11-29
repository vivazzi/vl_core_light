from django import template

from vl_core.utils.math import replace_comma_to_point, separate_thousand

register = template.Library()


@register.filter
def mod(number, value):
    return number % value


@register.filter(name='replace_comma_to_point')
def replace_comma_to_point_tag(value):
    return replace_comma_to_point(value)


@register.filter(name='separate_thousand')
def do_separate_thousand(value):
    return separate_thousand(value)
