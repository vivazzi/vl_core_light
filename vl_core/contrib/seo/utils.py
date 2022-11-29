from datetime import datetime
from os.path import join, exists

from django.conf import settings
from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import mail_admins
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _

from vl_core.conf import app_settings as core_app_settings
from vl_core.contrib.seo.conf import app_settings


class SitemapSet:
    """
        Dummy sitemap_set for inheritance
    """
    def get_static_urls(self):
        return []

    def get_sitemaps(self):
        return {}


sitemap_set = import_string(app_settings.SITEMAP_SET_CLASS)()


class AbstractSitemapClass:
    changefreq = 'weekly'
    url = None

    def get_absolute_url(self):
        return self.url


class StaticSitemap(Sitemap):
    def items(self):
        main_sitemaps = []

        for url in sitemap_set.get_static_urls():
            sitemap_class = AbstractSitemapClass()
            sitemap_class.url = url
            main_sitemaps.append(sitemap_class)

        return main_sitemaps

    lastmod = datetime.now().date()
    priority = 0.5
    changefreq = 'weekly'


def generate_sitemap_handler(request):
    sitemaps = sitemap_set.get_sitemaps()
    if sitemap_set.get_static_urls():
        sitemaps.update({'static_urls': StaticSitemap})

    with open(join(settings.ROOT_DIR, 'sitemap.xml'), 'w') as f:
        if sitemaps:
            xml = sitemap(request, sitemaps)
            f.write(xml.rendered_content)

    if not settings.DEBUG:
        for item in app_settings.NOTIFICATIONS_FOR_SEARCH_ENGINES:
            import_string(item)()


def get_robots_content():
    path = join(settings.ROOT_DIR, 'robots.txt')

    if not exists(path):
        current_site = get_current_site(None)
        robots_content = render_to_string('vl_seo/robots.txt', {'sitemap_path': app_settings.FULL_SITEMAP_PATH,
                                                                'host': f'{core_app_settings.PROTOCOL}://{current_site.domain}'})

        with open(path, 'w') as f:
            f.write(robots_content)

        mes = _('robots.txt created on the site "{}"').format(current_site.name)
        mail_admins(mes, _('{}. Previously, this file was missing or it was deleted').format(mes))

    with open(join(settings.ROOT_DIR, 'robots.txt')) as f:
        return f.read()


def get_sitemap_content(request):
    path = join(settings.ROOT_DIR, 'sitemap.xml')
    if not exists(path):
        generate_sitemap_handler(request)
        mes = _('Generated sitemap.xml on the site "{}"').format(get_current_site(None))
        mail_admins(mes, _('{}. Previously, this file was missing or it was deleted').format(mes))

    with open(path) as f:
        return f.read()
