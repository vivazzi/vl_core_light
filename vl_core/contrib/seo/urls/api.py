from django.conf import settings
from django.urls import path

from vl_core.contrib.seo.views import get_sitemap, get_robots, generate_sitemap_and_ping_search_engines

app_name = 'vl_seo_api'

# include to urlpatterns only
urlpatterns = [
    path('vl_admin/generic/', generate_sitemap_and_ping_search_engines, name='generic'),
]

if settings.DEBUG:
    urlpatterns = [
        path('sitemap.xml', get_sitemap),
        path('robots.txt', get_robots),
    ] + urlpatterns
