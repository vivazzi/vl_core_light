from functools import wraps
from urllib.parse import urljoin


# todo: may be it useless
def app_permalink(func):
    from django.urls import reverse, NoReverseMatch

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            bits = func(*args, **kwargs)
            return reverse(bits[0], None, *bits[1:3])
        except NoReverseMatch:
            pass

        return urljoin('/app_not_found/', args[0].slug)

    return inner
