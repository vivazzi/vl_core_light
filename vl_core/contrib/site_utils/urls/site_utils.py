from django.urls import path, include

from vl_core.contrib.site_utils.views import utils, site_utils_app

app_name = 'vl_site_utils'

# include to i18n_urls
urlpatterns = (
    path('vl_admin/site_utils_app/', site_utils_app, name='site_utils_app'),
    path('vl_admin/utils/', include([
        path('', utils, name='utils'),
        path('command-runner/', utils),
        path('performance/', utils),
        path('email-testing/', utils),
        path('used-components/', utils),
    ])),
)
