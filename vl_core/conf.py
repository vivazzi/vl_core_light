from django.conf import settings


# noinspection PyMethodMayBeStatic
class BaseAppSettings:

    def _setting(self, name, default=None, required=True):
        from django.conf import settings
        res = getattr(settings, name, default)

        if res is None and required:
            raise Exception(f'"{self.__module__.split(".")[0]}" app requires "{name}" in settings.py')

        return res

    def __getattr__(self, key):
        if not key.startswith('VL_'):
            key = f'VL_{key}'
        return self.__getattribute__(key)


# noinspection PyPep8Naming,PyUnresolvedReferences
class AppSettings(BaseAppSettings):

    @property
    def FRONTEND_DEV_PORT(self):
        return self._setting('VL_FRONTEND_DEV_PORT', 4000)

    @property
    def FRONTEND_DEV_MODE(self):
        return self._setting('VL_FRONTEND_DEV_MODE', False)

    @property
    def PROTOCOL(self):
        return self._setting('VL_PROTOCOL', 'http' if settings.DEBUG else 'https')


app_settings = AppSettings()
