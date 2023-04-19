from django.contrib.sites.shortcuts import get_current_site

from vl_core.conf import BaseAppSettings, app_settings as core_app_settings


# noinspection PyPep8Naming
class AppSettings(BaseAppSettings):

    @property
    def SITEMAP_SET_CLASS(self):
        return self._setting('VL_SITEMAP_SET_CLASS', 'vl_core.contrib.seo.utils.SitemapSet')

    @property
    def SITEMAP_URL(self):
        return self._setting('VL_SITEMAP_URL', '/sitemap.xml')

    @property
    def FULL_SITEMAP_PATH(self):
        def get_default_sitemap_path():
            return f'{core_app_settings.PROTOCOL}://{get_current_site(None).domain}{self.SITEMAP_URL}'

        return self._setting('VL_FULL_SITEMAP_PATH', get_default_sitemap_path())

    @property
    def NOTIFICATIONS_FOR_SEARCH_ENGINES(self):
        return self._setting('VL_NOTIFICATIONS_FOR_SEARCH_ENGINES', ['vl_core.contrib.seo.notifications.google.notify'])


app_settings = AppSettings()
