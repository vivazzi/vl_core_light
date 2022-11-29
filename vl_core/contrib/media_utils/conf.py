from vl_core.conf import BaseAppSettings


# noinspection PyPep8Naming
class AppSettings(BaseAppSettings):
    @property
    def USE_HINT_FOR_COMPRESSION(self):
        return self._setting('VL_USE_HINT_FOR_COMPRESSION', True)

    @property
    def PIC_FIELD_OPTIMIZE_PARS(self):
        return self._setting('VL_PIC_FIELD_OPTIMIZE_PARS', {'checked_by_default': True,
                                                            'max_size': {'width': 1366, 'height': 920},
                                                            'quality': 85})


app_settings = AppSettings()
