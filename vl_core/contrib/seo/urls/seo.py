from django.urls import path

from vl_core.contrib.seo.views import seo

app_name = 'vl_seo'

# include to i18n_urls
urlpatterns = (
    path('vl_admin/seo/', seo, name='seo'),
)
