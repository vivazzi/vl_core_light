import json
import os
from datetime import datetime, timedelta
from os import listdir
from os.path import join, exists, dirname, basename

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.http import JsonResponse, FileResponse, Http404
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import gettext as _

from vl_core.constants import FRONTEND_MANIFEST_PATH, FRONTEND_STATIC_URL_PREFIX
from vl_core.conf import app_settings as vl_core_app_settings
from vl_core.contrib.backup.conf import app_settings
from vl_core.contrib.backup.constants import NEED_BACKUP
from vl_core.contrib.backup.utils import backup_module
from vl_core.utils.core import convert_seconds, humanize_bytes
from vl_core.utils.os import get_size


@admin.site.admin_view
def backup_dashboard(request):
    context = {
        **admin.site.each_context(request),

        'title': _('Statistics and backups'),
        'config': {
            'manifest_path': FRONTEND_MANIFEST_PATH,
            'port': vl_core_app_settings.FRONTEND_DEV_PORT,
            'dev_mode': vl_core_app_settings.FRONTEND_DEV_MODE,
            'static_url_prefix': FRONTEND_STATIC_URL_PREFIX,
        },
    }

    return render(request, 'vl_backup/backup_dashboard.html', context)


@user_passes_test(lambda u: u.is_superuser)
def get_backups(request):
    lockfile_content = ''
    current_elapsed_time = 0

    next_backup_delta = ''
    next_backup_date = ''

    stat = backup_module.get_stat()

    if stat['backup_date'] != 0:
        next_backup_date = (datetime.fromtimestamp(stat['backup_date']) + timedelta(seconds=app_settings.BACKUP_INTERVAL))
        seconds = (next_backup_date - datetime.now()).total_seconds()
        if seconds < 0:
            seconds = 0

        next_backup_delta = convert_seconds(seconds)
        next_backup_date = next_backup_date.timestamp()

    # lockfile
    db_dir = join(dirname(settings.BASE_DIR), 'db')
    lockfile_path = join(db_dir, 'lockfile')
    if exists(lockfile_path):
        groups = []
        with open(lockfile_path, 'r', encoding='utf-8') as f:
            lockfile_content = f.read().strip()
            if '|' in lockfile_content:
                lockfile_now_timestamp, groups = lockfile_content.split('|')
                if groups != NEED_BACKUP:
                    if groups:
                        groups = groups.split(',')
                    current_elapsed_time = (datetime.now() - datetime.fromtimestamp(float(lockfile_now_timestamp))).total_seconds()

        existed_files = []
        for filename in listdir(db_dir):
            if filename.startswith('db') or filename.startswith('media') or filename.startswith('code'):
                can_download = True

                if filename not in stat['sizes']['backups']['files']:
                    if any([filename.startswith(group) for group in groups]):
                        can_download = False

                    size = get_size(join(db_dir, filename))
                    stat['sizes']['backups']['files'][filename] = {
                        'size': size,
                        'size_str': humanize_bytes(size),
                    }

                stat['sizes']['backups']['files'][filename].update({
                    'can_download': can_download,
                    'url': reverse('vl_backup_:download_file', args=(filename,)),
                })

                existed_files.append(filename)

        # remove absent files
        absent_files = []
        for filename in stat['sizes']['backups']['files']:
            if filename not in existed_files:
                absent_files.append(filename)

        for filename in absent_files:
            del stat['sizes']['backups']['files'][filename]

    else:
        for filename in stat['sizes']['backups']['files'].keys():
            stat['sizes']['backups']['files'][filename].update({
                'can_download': True,
                'url': reverse('vl_backup_api:download_file', args=(filename,)),
            })

    return JsonResponse({
        'status': 'ok',
        'lockfile_content': lockfile_content,
        'stat': stat,
        'next_backup_delta': next_backup_delta,
        'next_backup_date': next_backup_date,
        'current_elapsed_time': convert_seconds(current_elapsed_time) if current_elapsed_time else '',
    })


@user_passes_test(lambda u: u.is_superuser)
def download_file(request, name):
    name = basename(name)  # it helps exclude bad urls such as '../some_path/' and so on

    db_dir = join(dirname(settings.BASE_DIR), 'db')

    file_path = join(db_dir, name)
    if not exists(file_path):
        raise Http404(f'File "{file_path}" is not found')

    response = FileResponse(open(file_path, 'rb'), content_type='application/x-gzip')
    response['Content-Disposition'] = f'attachment; filename={name}'

    return response


@user_passes_test(lambda u: u.is_superuser)
def backup(request):
    db_dir = join(dirname(settings.BASE_DIR), 'db')
    if not exists(db_dir):
        os.makedirs(db_dir)

    lockfile_content = ''
    lockfile_path = join(db_dir, 'lockfile')
    if not exists(lockfile_path):
        lockfile_content = f'{datetime.now().timestamp()}|{NEED_BACKUP}'
        with open(lockfile_path, 'w', encoding='utf-8') as f:
            f.write(lockfile_content)

    return JsonResponse({'status': 'ok', 'lockfile_content': lockfile_content})


def backup_app(request):
    data = {
        'urls': {
            'backup': reverse('vl_backup_api:backup'),
            'get_given_size': app_settings.GET_GIVEN_SIZE_URL,
            'get_backups': reverse('vl_backup_api:get_backups'),
        },
        'config': {
            'backup_interval': convert_seconds(app_settings.BACKUP_INTERVAL),
            'backup_db_count': app_settings.BACKUP_DB_COUNT,
            'backup_media_count': app_settings.BACKUP_MEDIA_COUNT,
        }
    }

    return JsonResponse(data)
