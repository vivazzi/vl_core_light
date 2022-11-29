from django.urls import path, include

from vl_core.contrib.backup.views import backup_dashboard, backup_app

app_name = 'vl_backup'

# include to i18n_urls
urlpatterns = (
    path('vl_admin/', include([
        path('backup_dashboard/', backup_dashboard, name='backup_dashboard'),
        path('backup_app/', backup_app, name='backup_app'),
    ])),
)
