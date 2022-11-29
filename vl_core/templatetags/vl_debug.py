from django import template

register = template.Library()


@register.filter
def debug(v, p=None):
    print(f'v = {v}\n'
          f'p = {p}')
    return v
