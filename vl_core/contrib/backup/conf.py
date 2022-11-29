from vl_core.conf import BaseAppSettings


# noinspection PyPep8Naming
class AppSettings(BaseAppSettings):

    @property
    def GET_GIVEN_SIZE_URL(self):
        return self._setting('VL_GET_GIVEN_SIZE_URL', '')

    @property
    def BACKUP_INTERVAL(self):
        return self._setting('VL_BACKUP_INTERVAL', 24 * 3600)

    @property
    def BACKUP_TIMEOUT(self):
        return self._setting('VL_BACKUP_TIMEOUT', 2 * 3600)

    @property
    def BACKUP_DB_COUNT(self):
        return self._setting('VL_BACKUP_DB_COUNT', 1)

    @property
    def BACKUP_MEDIA_COUNT(self):
        return self._setting('VL_BACKUP_MEDIA_COUNT', 1)


app_settings = AppSettings()
