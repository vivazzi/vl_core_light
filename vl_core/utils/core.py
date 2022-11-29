import random
from datetime import timedelta
from typing import Union

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.management import call_command
from django.utils.translation import gettext as _

from vl_core.constants import ALPHABET_AND_DIGITS


def random_seq(length: int = 5, seq: str = ALPHABET_AND_DIGITS) -> str:
    # noinspection PyArgumentList
    return ''.join(random.choices(seq, k=length))


def unique_random_seq_for_model_field(model_class, par: str, excluded_obj=None, length: int = 5, seq: str = ALPHABET_AND_DIGITS) -> str:
    """
    Example:

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_unique_random_seq(self._meta.model, 'token', None, 40)

        return super().save(*args, **kwargs)
    """
    objects = model_class.objects
    if excluded_obj and excluded_obj.pk:
        if not isinstance(excluded_obj, model_class):
            # noinspection PyProtectedMember
            raise ImproperlyConfigured(f'"{excluded_obj._meta.object_name}" class of parameter "excluded_obj" is not equal '
                                       f'with model class ("{model_class._meta.object_name}"). "excluded_obj" must be same class type as model.')

        objects = objects.exclude(pk=excluded_obj.pk)

    count = 0
    max_count = 10000000000000000
    while count < max_count:
        field_value = random_seq(length, seq)
        if objects.filter(**{par: field_value}).count() == 0:
            return field_value

        count += 1

    raise Exception('get_unique_random_seq loops infinitely')


def send_mails_if_debug() -> None:
    if settings.DEBUG and settings.EMAIL_BACKEND == 'post_office.EmailBackend':
        call_command('send_queued_mail')


def without_zero(value: Union[None, str, float]) -> str:
    """
    Remove useless zeros in number
    Examples:

    >>> without_zero(1.0)
    '1'
    >>> without_zero('1.0')
    '1'
    >>> without_zero('01.050')
    '1.05'

    :param value: string or number
    :return: number string without useless zeros
    """
    if value is None:
        return ''

    value = str(value).replace(',', '.')
    if '.' in value:
        value = value.strip('0')

        if value[0] == '.': value = f'0{value}'
        if value[-1] == '.': value = value[:-1]

    return value


# noinspection SpellCheckingInspection
def humanize_bytes(n: int, precision: int = 2) -> str:
    # Author: Doug Latornell
    # Licence: MIT
    # URL: http://code.activestate.com/recipes/577081/
    """Return a humanized string representation of a number of bytes.

    >>> humanize_bytes(1)
    '1 B'
    >>> humanize_bytes(1024, precision=1)
    '1.0 KB'
    >>> humanize_bytes(1024 * 123, precision=1)
    '123.0 KB'
    >>> humanize_bytes(1024 * 12342, precision=1)
    '12.1 MB'
    >>> humanize_bytes(1024 * 12342, precision=2)
    '12.05 MB'
    >>> humanize_bytes(1024 * 1234, precision=2)
    '1.21 MB'
    >>> humanize_bytes(1024 * 1234 * 1111, precision=2)
    '1.31 GB'
    >>> humanize_bytes(1024 * 1234 * 1111, precision=1)
    '1.3 GB'

    """
    abbrevs = [
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'KB'),
        (1, 'B')
    ]

    if n == 1:
        return '1 B'

    for factor, suffix in abbrevs:
        if n >= factor:
            break

    # noinspection PyUnboundLocalVariable
    return '%.*f %s' % (precision, float(n) / factor, suffix)


def convert_seconds(seconds: Union[float, timedelta], sec_precision: int = 0, sec_precision_for_small_time: int = 4,
                    exclude_minutes: bool = False, exclude_hours: bool = False, exclude_days: bool = False, exclude_weeks: bool = False,
                    round_by_minutes: bool = False, round_by_hours: bool = False, round_by_days: bool = False, round_by_weeks: bool = False) -> str:
    """
    Examples:

    >>> convert_seconds(0.12345)
    '0.1234 sec.'
    >>> convert_seconds(1.12345, sec_precision_for_small_time=2)
    '1.12 sec.'
    >>> convert_seconds(61.12345, sec_precision=1)
    '1 m. 1.1 sec.'
    >>> convert_seconds(61.12345, sec_precision=1, sec_precision_for_small_time=1)
    '1 m. 1.1 sec.'
    >>> convert_seconds(694861)
    '1 w. 1 d. 1 h. 1 m. 1 sec.'
    >>> convert_seconds(90001, exclude_days=False)  # do not use days (and weeks accordingly)
    '25 h. 0 m. 1 sec.'
    >>> convert_seconds(90060, exclude_hours=True)  # do not use hours (minutes and seconds accordingly); 90060 secs = 1 days 1 hours and 1 minute
    '1501 m. 0 sec.'

    :param seconds: time duration in seconds or timedelta object
    :param sec_precision: this presicion will be apply, if time duration more 1 minute
    :param sec_precision_for_small_time: this presicion will be applied, if time duration less 1 minute
    :param exclude_minutes: if False, then minutes, hours, days and weeks will not be used
    :param exclude_hours: if True, then hours, days and weeks will not be used
    :param exclude_days: if True, then days and weeks will not be used
    :param exclude_weeks: if True, then weeks will not be used
    :param round_by_minutes: if True, round by minutes (by floor)
    :param round_by_hours: if True, round by hours (by floor)
    :param round_by_days: if True, round by days (by floor)
    :param round_by_weeks: if True, round by weeks (by floor)
    :return: formatted string of time duration
    """
    if isinstance(seconds, timedelta):
        seconds = seconds.total_seconds()

    neg_sign = '-' if seconds < 0 else ''
    if seconds < 0:
        seconds *= -1

    w = d = h = m = 0
    sec = seconds

    if not exclude_minutes:
        m, sec = divmod(seconds, 60)

        if not exclude_hours:
            h, m = divmod(m, 60)

            if not exclude_days:
                d, h = divmod(h, 24)

                if not exclude_weeks:
                    w, d = divmod(d, 7)

    res = []

    check = lambda x: x or not x and bool(res)  # to exclude zero days, minutes and etc before at the beginning of result string

    if check(w): res.append((int(w), _('w')))
    if check(d): res.append((int(d), _('d')))
    if check(h): res.append((int(h), _('h')))
    if check(m): res.append((int(m), _('m')))

    sec = int(sec) if sec_precision == 0 else round(sec, sec_precision)
    res.append([sec, _('sec')])

    if len(res) == 1:
        res[0][0] = int(seconds) if sec_precision_for_small_time == 0 else round(seconds, sec_precision_for_small_time)

    if round_by_weeks: round_by_days = True
    if round_by_days: round_by_hours = True
    if round_by_hours: round_by_minutes = True

    check = lambda x: x and bool(res)  # do not touch res with 1 elements

    if check(round_by_minutes): del res[-1]
    if check(round_by_hours): del res[-1]
    if check(round_by_days): del res[-1]
    if check(round_by_weeks): del res[-1]

    if not res:
        if round_by_weeks: res.append((0, _('w')))
        elif round_by_days: res.append((0, _('d')))
        elif round_by_hours: res.append((0, _('h')))
        elif round_by_minutes: res.append((0, _('m')))

    return '%s%s' % (neg_sign, ' '.join(f'{" ".join(map(str, i))}.' for i in res))
