from django.views import defaults

ERROR_400_TEMPLATE_NAME = 'vl_core/errs/400.html'
ERROR_403_TEMPLATE_NAME = 'vl_core/errs/403.html'
ERROR_404_TEMPLATE_NAME = 'vl_core/errs/404.html'
ERROR_500_TEMPLATE_NAME = 'vl_core/errs/500.html'


def bad_request(request, exception=None, template_name=ERROR_400_TEMPLATE_NAME):
    return defaults.bad_request(request, exception, template_name)


def permission_denied(request, exception=None, template_name=ERROR_403_TEMPLATE_NAME):
    return defaults.permission_denied(request, exception, template_name)


def page_not_found(request, exception=None, template_name=ERROR_404_TEMPLATE_NAME):
    return defaults.page_not_found(request, exception, template_name)


def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    return defaults.server_error(request, template_name)
