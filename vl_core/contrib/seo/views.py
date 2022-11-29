import xml.dom.minidom

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext as _

from vl_core.contrib.seo.utils import generate_sitemap_handler, get_robots_content, get_sitemap_content
from vl_core.utils.url import with_domain


@admin.site.admin_view
def seo(request):
    def _get_sitemap_content():
        # noinspection PyBroadException
        try:
            return xml.dom.minidom.parseString(get_sitemap_content(request)).toprettyxml()
        except Exception:
            return _('Empty')

    ctx = {
        **admin.site.each_context(request),

        'title': 'SEO',
        'robots': {
            'url': with_domain('robots.txt'),
            'content': get_robots_content(),
        },
        'sitemap': {
            'url': with_domain('sitemap.xml'),
            'content': _get_sitemap_content(),
        }
    }

    return render(request, 'vl_seo/seo.html', ctx)


@user_passes_test(lambda u: u.is_staff)
def generate_sitemap_and_ping_search_engines(request):
    generate_sitemap_handler(request)

    if settings.DEBUG:
        mes = _('Generated sitemap without notifying search engines, since DEBUG mode is enabled')
    else:
        mes = _('Generated sitemap with notification to search engines')

    messages.success(request, mes)

    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])

    return redirect('/')


def get_robots(request):
    return HttpResponse(get_robots_content(), content_type='text/plain')


def get_sitemap(request):
    return HttpResponse(get_sitemap_content(request), content_type='application/xml')
