from os.path import exists, join

from django.utils.text import slugify
from unidecode import unidecode

from vl_core.contrib.media_utils.conf import app_settings
from vl_core.contrib.media_utils.constants import DIGITS_AND_ALPHABET_LOWER
from vl_core.utils.core import random_seq


def upload_to_handler(instance, filename):
    """
        If there are many objects in upload folder, then maybe loop while do a long time, so after some trying,
        we increase length to find unique folder fastly.

        We can use length equal is 4, sense it get 1,679,616 combinations - is enough large count.
        After 10 tryings length will be 5 and get 60,466,176 combinations and so on.

        :return: file path with unique folder name
    """

    filename = '.'.join(slugify(p) for p in unidecode(filename).split('.'))
    upload_to = instance.upload_to

    length = getattr(instance, 'UPLOAD_TO_HANDLER_FOLDER_LENGTH', 4)
    max_length = length + 6
    trying = 0
    max_trying = None
    while True:
        folder = random_seq(length, seq=DIGITS_AND_ALPHABET_LOWER)

        if not exists(join(upload_to, folder)):
            return join(upload_to, folder, filename)

        trying += 1

        if trying > 10 and length <= max_length:
            length += 1

        if not max_trying:
            max_trying = 10 ** 5

        if trying > max_trying:
            raise Exception('Max loop counter in upload_to_handler!')


def default_compress_settings(pic):
    attrs = {'optimize': True}
    if pic.mode in ('RGB', 'L', 'CMYK'):
        attrs.update({'format': 'JPEG', 'quality': app_settings.PIC_FIELD_OPTIMIZE_PARS['quality']})
    else:
        attrs.update({'format': 'PNG', 'quality': 100})  # 100 is the longest by time, but the most compressed

    return attrs
