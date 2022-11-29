from django.urls import path, include

from vl_core.contrib.site_utils.views import get_used_components, send_test_letter, speed_up, RunManagementCommandView

app_name = 'vl_site_utils_api'

# include to urlpatterns only
urlpatterns = (
    path('vl_admin/utils/', include([
        path('get_used_components/', get_used_components, name='get_used_components'),
        path('send_test_letter/', send_test_letter, name='send_test_letter'),
        path('speed_up/', speed_up, name='speed_up'),
        path('run_command/', RunManagementCommandView.as_view(), name='run_command'),
    ])),
)
