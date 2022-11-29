from django.core.management.base import BaseCommand
from vl_core.contrib.backup.utils import backup_module


class Command(BaseCommand):
    help = 'Backup db, media and code.'

    def handle(self, *args, **options):
        backup_module.backup()
