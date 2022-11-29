import io
import sys
import time

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import linebreaks
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from django.core import management
from django.core.management import CommandError

from django.views import View

from vl_core.constants import FRONTEND_MANIFEST_PATH, FRONTEND_STATIC_URL_PREFIX
from vl_core.conf import app_settings as vl_core_app_settings
from vl_core.contrib.site_utils.conf import app_settings
from vl_core.contrib.site_utils.forms import RunManagementCommandForm
from vl_core.utils.core import send_mails_if_debug, convert_seconds


@admin.site.admin_view
def utils(request):
    ctx = {
        **admin.site.each_context(request),

        'title': _('Site utilities'),
        'config': {
            'manifest_path': FRONTEND_MANIFEST_PATH,
            'port': vl_core_app_settings.FRONTEND_DEV_PORT,
            'dev_mode': vl_core_app_settings.FRONTEND_DEV_MODE,
            'static_url_prefix': FRONTEND_STATIC_URL_PREFIX,
        },
    }
    return render(request, 'vl_site_utils/site_utils.html', ctx)


@user_passes_test(lambda u: u.is_staff)
def get_used_components(request):
    components = []
    unused_components = []
    return JsonResponse({'components': components, 'unused_components': unused_components})


@user_passes_test(lambda u: u.is_staff)
def send_test_letter(request):
    def send_email():
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.smtp.EmailBackend':
            from django.core.mail import EmailMessage
            email = EmailMessage(subject, message, me, (request.user.email,), headers=headers)
            email.content_subtype = 'html'
            email.send()

        if settings.EMAIL_BACKEND == 'post_office.EmailBackend':
            from post_office import mail
            mail.send(request.user.email, me, subject=subject, html_message=message, headers=headers)
            send_mails_if_debug()

    me = f'<{settings.EMAIL_HOST_USER}>'
    subject = 'Test message'

    message = _('<p><strong>Test html message. This text must be bold</strong>.<br/>'
                'If it is true, then letter was received correctly.</p>')

    headers = {'To': f'{request.user.get_full_name()} <{request.user.email}>'}

    send_email()

    return JsonResponse({'status': 'ok'})


@user_passes_test(lambda u: u.is_staff)
def speed_up(request):
    results = {'accelerated': False}

    for item in app_settings.SITE_SPEED_UP_ENGINES:
        obj = import_string(item)()
        results.update(obj.speed_up())

        if obj.accelerated:
            results['accelerated'] = True

    return JsonResponse({'status': 'ok', 'results': results})


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class RunManagementCommandView(View):
    form = RunManagementCommandForm

    @property
    def command_help_list(self):
        res = {}
        for command, app in management.get_commands().items():
            try:
                command_class = management.load_command_class(app, command)
                parser = command_class.create_parser('', f'{command} (of {app} app)')
                res[f'{app}.{command}'] = {'desc': parser.format_help(),
                                           'option_help': parser.description,
                                           'command': command}
            except ImportError as e:
                sys.stderr.write(f'[WARNING] {e} | command "{command}" (of {app} app)\n')
        return res

    @staticmethod
    def str_to_args(string):
        row_params = string.split()
        params = []
        i = -1
        for par in row_params:
            if par.startswith('-'):
                params.append(par)
                i += 1
            else:
                params[i] += f'={par}'

        return params

    def get(self, request, *args, **kwargs):
        commands = self.command_help_list
        return JsonResponse({'commands': commands,
                             'selected_command': 'core.fix' if 'core.fix' in commands else list(commands.keys())[0]})

    def post(self, request, *args, **kwargs):
        ctx = {'status': 'fail'}
        form = self.form(request.POST)

        if form.is_valid():
            ctx.update({'status': 'fail', 'message': form.errors})

            parts = form.cleaned_data['command'].split('.')
            command = parts[-1]
            try:
                out = io.StringIO()
                t_start = time.time()
                management.call_command(command, stdout=out, *self.str_to_args(form.cleaned_data['params']))
                ctx.update({'status': 'ok',
                            'result': linebreaks(out.getvalue()),
                            'elapsed_time': convert_seconds(time.time() - t_start),
                            'message': _('"{}" command executed').format(command)})
            except CommandError as mes:
                ctx.update({'status': 'fail', 'message': mes})
            except SystemExit:
                ctx.update({'status': 'ok', 'message': _('"{}" command executed with standard option').format(command)})

        return JsonResponse(ctx)


def site_utils_app(request):
    data = {
        'urls': {
            'base_menu': reverse('vl_site_utils:utils'),

            'get_used_components': reverse('vl_site_utils_api:get_used_components'),
            'send_test_letter': reverse('vl_site_utils_api:send_test_letter'),
            'speed_up': reverse('vl_site_utils_api:speed_up'),
            'run_command': reverse('vl_site_utils_api:run_command'),
        },
        'config': {
            'testing_email': request.user.email,
        }
    }

    return JsonResponse(data)
