from django.core.management.base import BaseCommand

from django.http import HttpRequest

from vl_core.conf import app_settings
from vl_core.contrib.seo.utils import generate_sitemap_handler


class DummyUser:
    def __init__(self):
        self.is_staff = False
        self.is_authenticated = False


class DummyHttpRequest(HttpRequest):
    user = DummyUser()

    def _get_scheme(self):
        return app_settings.PROTOCOL


class Command(BaseCommand):
    help = 'Sitemap generation'

    def handle(self, *args, **options):
        generate_sitemap_handler(DummyHttpRequest())
