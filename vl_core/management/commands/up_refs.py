import json
from os.path import join, exists

from django.conf import settings
from django.core.management.base import BaseCommand


class AppDoesNotFound(Exception):
    pass


def get_repo_dir(app):
    local_pipfile_path = join(settings.BASE_DIR, 'local', 'Pipfile')
    if not exists(local_pipfile_path):
        raise Exception(f'You need has {local_pipfile_path}')

    with open(local_pipfile_path, 'r', encoding='utf-8') as f:
        for line in f:
            if app in line or app.replace('-', '_') in line:
                return line.rsplit('= ', maxsplit=1)[-1].replace('}', '').replace('"', '').strip()

    raise AppDoesNotFound


class Command(BaseCommand):
    help = 'Update version of refs of repositories from local path'

    def handle(self, *args, **options):
        pipfile_lock_path = join(settings.BASE_DIR, 'Pipfile.lock')

        with open(pipfile_lock_path, 'r', encoding='utf-8') as f:
            lock = json.loads(f.read())

        # find apps
        pipfile_path = join(settings.BASE_DIR, 'Pipfile')
        with open(pipfile_path, 'r', encoding='utf-8') as f:
            apps = [line.split(' ', maxsplit=1)[0].replace('_', '-') for line in f if ', git =' in line]

        for app in apps:
            old_ref = lock['default'][app]['ref']

            try:
                with open(join(get_repo_dir(app), '.git', 'refs', 'heads', 'master'), 'r', encoding='utf-8') as f:
                    new_ref = f.read().strip()

                if old_ref != new_ref:
                    with open(pipfile_lock_path, 'w', encoding='utf-8') as f:
                        lock['default'][app]['ref'] = new_ref
                        f.write(f'{json.dumps(lock, indent=4, sort_keys=True)}\n')
            except AppDoesNotFound:
                print(f'{app} is not found')
