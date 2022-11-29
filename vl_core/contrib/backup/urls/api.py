from django.urls import path, include

from vl_core.contrib.backup.views import download_file, get_backups, backup

app_name = 'vl_backup_api'

# include to urlpatterns only
urlpatterns = (
    path('vl_admin/backup/', include([
        path('download_file/<name>/', download_file, name='download_file'),
        path('get_backups/', get_backups, name='get_backups'),
        path('backup/', backup, name='backup'),
    ])),
)
