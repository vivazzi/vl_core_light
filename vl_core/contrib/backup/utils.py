import json
import os
import shutil
import time
from datetime import datetime
from functools import cached_property
from os import listdir
from os.path import join, dirname, exists, getmtime, basename, isfile
from subprocess import Popen, run, PIPE

from django.conf import settings

from vl_core.contrib.backup.conf import app_settings
from vl_core.contrib.backup.constants import NOW_STR_FORMAT, NEED_BACKUP
from vl_core.utils.core import humanize_bytes, convert_seconds
from vl_core.utils.os import get_size, get_free_space, apply_func_to_file_in_folder


def format_line(line):
    line = line.replace('\n', '').replace('*', r'\s*')
    result = f'{line}$'
    if not result.startswith(r'\s*'):
        result = f'^{result}'
    return result


def copy_file(old_path, new_dir_path, delete_path=''):
    if not delete_path:
        delete_path = dirname(new_dir_path)

    rel = old_path.replace(delete_path, '')
    if rel[0] == '/':
        rel = rel[1:]

    new_path = join(new_dir_path, rel)

    if not exists(dirname(new_path)):
        os.makedirs(dirname(new_path))

    shutil.copyfile(old_path, new_path)


class BackupModule:
    def __init__(self):
        self.common_dir = dirname(settings.ROOT_DIR)
        self.db_dir = join(dirname(settings.ROOT_DIR), 'db')
        self.stat_path = join(self.db_dir, 'stat')
        self.project_name = basename(settings.ROOT_DIR)

        self.stat = self.initial_stat

    @property
    def initial_stat(self):
        return {
            'sizes': {
                'db': 0, 'db_str': '',
                'media': 0, 'media_str': '',
                'code': 0, 'code_str': '',
                'backups': {
                    'total': 0,
                    'files': {
                        # some files. Real date instead of %d_%m_%Y__%H_%M_%S
                        # 'db_project_%d_%m_%Y__%H_%M_%S.tar.gz': {'size': 0, 'size_str': ''},
                        # 'media_project_%d_%m_%Y__%H_%M_%S.tar.gz': {'size': 0, 'size_str': ''},
                        # 'code_project_%d_%m_%Y__%H_%M_%S.tar.gz': {'size': 0, 'size_str': ''}
                    }
                },
                'total': 0,
            },
            'backup_date': 0,
            'backup_date_str': '',
            'elapsed_time': 0,
            'code_ref': '',
        }

    def _set_actual_parameters(self):
        self.t0 = time.time()  # for the calculating of elapsed time
        self.now = datetime.now()
        self.get_stat()

    @property
    def now_str(self):
        return self.now.strftime(NOW_STR_FORMAT)

    @property
    def now_timestamp(self):
        return self.now.timestamp()

    @cached_property
    def venv_path(self):
        os.environ['PIPENV_IGNORE_VIRTUALENVS'] = '1'
        result = run('pipenv --venv', stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True, cwd=settings.ROOT_DIR)
        if result.stderr:
            raise Exception(f'ERROR: {result.stderr}')

        return str(result.stdout).split('\n')[0]

    def get_stat(self):
        if exists(self.stat_path):
            with open(self.stat_path, 'r', encoding='utf-8') as f:
                self.stat = json.loads(f.read().strip())
        else:
            self.stat = self.initial_stat

        return self.stat

    def _create_db_backup(self, out):
        db_filename = f'db_{self.project_name}_{self.now_str}'
        backup_path = join(self.db_dir, db_filename)
        out.write('Create db backup\n')
        p = Popen(f'pg_dump -U {settings.DB_USER} -F c -f {backup_path} {settings.DATABASES["default"]["NAME"]}',
                  stdout=out, stderr=out, shell=True)
        p.wait()

        self.stat['sizes']['db'] = get_size(backup_path)

        # backup to tar
        out.write('Archive db backup\n')
        tar_path = join(self.db_dir, f'db_{self.project_name}_{self.now_str}.tar.gz')
        p = Popen(f'tar -czf {tar_path} -C {self.db_dir} {db_filename}', stdout=out, stderr=out, shell=True)
        p.wait()
        os.remove(backup_path)

        return tar_path, self.stat

    def _create_media_backup(self, out):
        out.write('Archive media backup\n')
        tar_path = join(self.db_dir, f'media_{self.project_name}_{self.now_str}.tar.gz')
        p = Popen(f'tar -czf {tar_path} -C {settings.ROOT_DIR} media', stdout=out, stderr=out, shell=True)
        p.wait()

        return tar_path

    def _create_code_backup(self, out):
        out.write('Check code backup\n')

        current_code_ref = None
        master_path = join(settings.ROOT_DIR, '.git', 'refs', 'heads', 'master')
        if exists(master_path):
            with open(master_path, 'r', encoding='utf-8') as f:
                current_code_ref = f.read().strip()

        if not current_code_ref or 'code_ref' not in self.stat or 'code_ref' in self.stat and self.stat['code_ref'] != current_code_ref:
            out.write('Archive code backup\n')

            ignore_patterns = ['^.git$', '^collect_static$', '^media$', '^uwsgi.sock$']

            with open(join(settings.ROOT_DIR, '.gitignore')) as f:
                for line in f:
                    if not line.startswith('\n') and not line.startswith('#'):
                        ignore_patterns.append(format_line(line))

            # create temp folder
            temp_folder = f'code_{self.project_name}'
            temp_folder_with_date = f'{temp_folder}_{self.now_str}'
            temp_dir = join(settings.ROOT_DIR, temp_folder_with_date)

            if exists(temp_dir):
                shutil.rmtree(temp_dir)

            os.mkdir(temp_dir)
            ignore_patterns.append(f'^{temp_folder}')

            apply_func_to_file_in_folder(settings.ROOT_DIR, True, ignore_patterns, False, copy_file, temp_dir)

            # create excluded collect_static and media folder
            os.mkdir(join(temp_dir, 'collect_static'))
            with open(join(temp_dir, 'collect_static', 'placeholder'), 'w', encoding='utf-8'):
                pass

            os.mkdir(join(temp_dir, 'media'))
            with open(join(temp_dir, 'media', 'placeholder'), 'w', encoding='utf-8'):
                pass

            # copy sbl plugins
            with open(join(settings.ROOT_DIR, 'Pipfile'), 'r', encoding='utf-8') as f:
                for line in f:
                    if 'VL_USERNAME' in line:
                        app = line.split(' ')[0]
                        venv_base_path = join(self.venv_path, 'src', app.replace('_', '-'))
                        apply_func_to_file_in_folder(join(venv_base_path, app), True, ignore_patterns, False,
                                                     copy_file, temp_dir, venv_base_path)

            # archive temp_dir
            tar_name = f'code_{self.project_name}_{self.now_str}.tar.gz'
            tar_path = join(self.db_dir, tar_name)
            p = Popen(f'tar -czf {tar_path} -C {settings.ROOT_DIR} {basename(temp_dir)}', stdout=out, stderr=out, shell=True)
            p.wait()

            # delete temp_dir
            shutil.rmtree(temp_dir)

            # delete old code backup archive
            for filename in listdir(self.db_dir):
                if filename.startswith('code') and filename != tar_name and isfile(join(self.db_dir, filename)):
                    os.remove(join(self.db_dir, filename))

            self.stat['code_ref'] = current_code_ref
        else:
            out.write('Code backup is up to date\n')

    def _delete_extra_limit_files(self, count, starts_with):
        files = [{'name': filename, 'creation_date': self._get_created_date(filename)} for filename in listdir(self.db_dir) if
                 filename.startswith(starts_with)]
        need_to_delete_files = sorted(files, key=lambda x: x['creation_date'], reverse=True)[count:]

        for file in need_to_delete_files:
            os.remove(join(self.db_dir, file['name']))

    def _save_lockfile(self, lockfile_path, additional_pars=''):
        with open(lockfile_path, 'w', encoding='utf-8') as f:
            f.write(f'{self.now_timestamp}|{additional_pars}')

    def _get_created_date(self, filename):
        """
            Get date (timestamp) from filename
            # db_sbl_28_06_2021__15_04_08.tar.gz -> 28_06_2021__15_04_08 (datetime) -> 1625371584 (timestamp)
        """
        date = filename.split('.')[0]
        date = date.replace('db', '').replace('media', '').replace('code', '').replace(self.project_name, '').replace('__', '', 1)
        return datetime.strptime(date, NOW_STR_FORMAT).timestamp()

    def _update_stat(self):
        # noinspection PyTypeChecker
        self.stat['backup_date'] = self.now_timestamp

        # get media size
        self.stat['sizes']['media'] = get_size(join(settings.ROOT_DIR, 'media'))

        # get code size
        self.stat['sizes']['code'] = 0

        if not settings.DEBUG:
            for item_name in listdir(self.common_dir):
                if item_name not in ('db', self.project_name):
                    self.stat['sizes']['code'] += get_size(join(self.common_dir, item_name))

        for item_name in listdir(settings.ROOT_DIR):
            if item_name not in ('media',):
                self.stat['sizes']['code'] += get_size(join(settings.ROOT_DIR, item_name))

        self.stat['sizes']['code'] += get_size(self.venv_path)

        # get backup sizes
        self.stat['sizes']['backups']['total'] = 0

        files = {}
        for filename in listdir(self.db_dir):
            if filename.startswith('db') or filename.startswith('media') or filename.startswith('code'):
                # noinspection PyTypeChecker
                files[filename] = {
                    'size': self.stat['sizes']['backups']['files'][filename]['size'] if filename in self.stat['sizes']['backups'][
                        'files'] else get_size(join(self.db_dir, filename)),
                    'created_date': self._get_created_date(filename),
                }
                self.stat['sizes']['backups']['total'] += files[filename]['size']

        self.stat['sizes']['backups']['files'] = files

        # calc total size
        self.stat['sizes']['total'] = (self.stat['sizes']['db'] + self.stat['sizes']['media'] + self.stat['sizes']['code'] +
                                       self.stat['sizes']['backups']['total'])

        # add human representation
        for item in ('db', 'media', 'code', 'total'):
            self.stat['sizes'][f'{item}_str'] = humanize_bytes(self.stat['sizes'][item])

        self.stat['sizes']['backups']['total_str'] = humanize_bytes(self.stat['sizes']['backups']['total'])

        for key in self.stat['sizes']['backups']['files'].keys():
            # noinspection PyTypeChecker
            self.stat['sizes']['backups']['files'][key]['size_str'] = humanize_bytes(self.stat['sizes']['backups']['files'][key]['size'])

        self.stat['backup_date_str'] = self.now.strftime('%d.%m.%Y %H:%M:%S')

        # save elapsed_time
        elapsed_time = time.time() - self.t0
        # noinspection PyTypeChecker
        self.stat['elapsed_time'] = elapsed_time
        self.stat['elapsed_time_str'] = convert_seconds(elapsed_time)

        self._save_stat()

        return elapsed_time

    def _save_stat(self):
        with open(self.stat_path, 'w', encoding='utf-8') as f:
            f.write(f'{json.dumps(self.stat, indent=4, sort_keys=True)}\n')

    def _check_free_space(self):
        if 'db' in self.stat['sizes']:
            free_space = get_free_space()
            max_size = max(self.stat['sizes']['db'], self.stat['sizes']['media'], self.stat['sizes']['code'])
            if max_size * 1.5 > free_space:
                low_space_message = f'ERROR: Backup is not created, ' \
                                    f'sense free space on server is low (need more {humanize_bytes(max_size)})'

                print(low_space_message)

                if (
                        'errors' not in self.stat or
                        'errors' in self.stat and (self.stat['errors']['date'] + 24 * 3600) < self.now_timestamp
                ):
                    self.stat['errors'] = {'type': 'low_space', 'date': self.now_timestamp}
                    self._save_stat()

                    raise Exception(low_space_message)

                return False

            if 'errors' in self.stat:
                del self.stat['errors']

        return True

    def backup(self):
        if 'WORKON_HOME' not in os.environ:
            raise Exception('ERROR: you need to add WORKON_HOME in os environment')

        if not exists(self.db_dir):
            os.mkdir(self.db_dir)

        self._set_actual_parameters()

        lockfile_content = ''
        lockfile_path = join(self.db_dir, 'lockfile')
        if exists(lockfile_path):
            with open(lockfile_path, 'r', encoding='utf-8') as f:
                need_backup_timestamp, lockfile_content = f.read().strip().split('|')
                need_backup_timestamp = float(need_backup_timestamp)

        if (
                NEED_BACKUP in lockfile_content or
                not lockfile_content and (self.now_timestamp - self.stat['backup_date']) > app_settings.BACKUP_INTERVAL or
                exists(lockfile_path) and (need_backup_timestamp - getmtime(lockfile_path)) > app_settings.BACKUP_TIMEOUT
        ):
            if not self._check_free_space():
                return

            log_dir = join(self.common_dir, 'logs')
            if not exists(log_dir):
                os.mkdir(log_dir)

            with open(join(log_dir, 'backup.log'), 'a') as out:
                out.write(f'\n--- START BACKUP ({self.now_str}) ---\n')

                self._save_lockfile(lockfile_path, 'db,media,code')

                # create backups
                db_tar_path = self._create_db_backup(out)
                self._save_lockfile(lockfile_path, 'media,code')
                self._delete_extra_limit_files(app_settings.BACKUP_DB_COUNT, 'db_')

                media_tar_path = self._create_media_backup(out)
                self._save_lockfile(lockfile_path, 'code')
                self._delete_extra_limit_files(app_settings.BACKUP_MEDIA_COUNT, 'media_')

                self._create_code_backup(out)
                self._save_lockfile(lockfile_path, '')

                # send backups to remote servers
                if settings.BACKUPS:
                    out.write('Send backups to remote servers\n')
                    for backup in settings.BACKUPS:
                        remote_db_dir = join('/home', backup["user"], 'backups', self.project_name)
                        address = f'{backup["user"]}@{backup["host"]}'

                        # creation db folder of project
                        p = Popen(f'ssh {address} mkdir -p {remote_db_dir}', shell=True)
                        p.wait()

                        # copying db and media to db folder of project
                        # noinspection SpellCheckingInspection
                        Popen(f'rsync -za -e ssh --numeric-ids --bwlimit=10000 {db_tar_path} {address}:{remote_db_dir}',
                              stdout=out, stderr=out, shell=True)
                        # noinspection SpellCheckingInspection
                        Popen(f'rsync -za -e ssh --numeric-ids --bwlimit=10000 {media_tar_path} {address}:{remote_db_dir}',
                              stdout=out, stderr=out, shell=True)

                elapsed_time = self._update_stat()

                # delete lockfile
                os.remove(lockfile_path)

                # show elapsed time
                out.write(f'--- END: elapsed time: {convert_seconds(elapsed_time)} ---\n')


backup_module = BackupModule()
