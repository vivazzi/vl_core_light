from django.contrib.sitemaps import ping_google

from vl_core.contrib.seo.conf import app_settings


def notify():
    ping_google(app_settings.SITEMAP_URL)
