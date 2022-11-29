from vl_core.conf import BaseAppSettings


# noinspection PyPep8Naming
class AppSettings(BaseAppSettings):

    @property
    def SITE_SPEED_UP_ENGINES(self):
        return self._setting('VL_SITE_SPEED_UP_ENGINES', ['vl_core.contrib.site_utils.speed_up_utils.RemoveNbspFromTextPlugin'])


app_settings = AppSettings()
