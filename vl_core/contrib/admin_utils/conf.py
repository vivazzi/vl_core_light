from vl_core.conf import BaseAppSettings


# noinspection PyPep8Naming
class AppSettings(BaseAppSettings):
    @property
    def ADMIN_TOOLS_THEMING_CSS(self):
        return self._setting('VL_ADMIN_TOOLS_THEMING_CSS', 'vl_admin_utils/theming.css')

    @property
    def ADMIN_FAVICON_URL(self):
        return self._setting('VL_ADMIN_FAVICON_URL', 'vl_admin_utils/favicon.svg')


app_settings = AppSettings()
