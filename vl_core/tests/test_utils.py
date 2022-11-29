from django.test import TestCase

from vl_core.constants import ALPHABET_AND_DIGITS
from vl_core.utils.core import without_zero, humanize_bytes, convert_seconds, random_seq


class UtilTest(TestCase):
    maxDiff = None

    def test_random_seq(self):
        seq = random_seq(length=5, seq=ALPHABET_AND_DIGITS)

        self.assertEqual(5, len(seq))

        for char in seq:
            with self.subTest(i=char):
                self.assertTrue(char in ALPHABET_AND_DIGITS)

    def test_without_zero(self):
        self.assertEqual('1', without_zero(1.0))
        self.assertEqual('1', without_zero('1.0'))
        self.assertEqual('1.05', without_zero('01.050'))
        self.assertEqual('0.05', without_zero('00.050'))
        self.assertEqual('0', without_zero('0'))
        self.assertEqual('0', without_zero('0.0'))
        self.assertEqual('', without_zero(None))

    def test_humanize_bytes(self):
        self.assertEqual('1 B', humanize_bytes(1))
        self.assertEqual('1.0 KB', humanize_bytes(1024, precision=1))
        self.assertEqual('123.0 KB', humanize_bytes(1024 * 123, precision=1))
        self.assertEqual('12.1 MB', humanize_bytes(1024 * 12342, precision=1))
        self.assertEqual('12.05 MB', humanize_bytes(1024 * 12342, precision=2))
        self.assertEqual('1.21 MB', humanize_bytes(1024 * 1234, precision=2))
        self.assertEqual('1.31 GB', humanize_bytes(1024 * 1234 * 1111, precision=2))
        self.assertEqual('1.3 GB', humanize_bytes(1024 * 1234 * 1111, precision=1))

    def test_convert_seconds(self):
        second = 1
        minute = 60 * second
        hour = 60 * minute
        day = 24 * hour
        week = 7 * day

        # small seconds
        self.assertEqual('0.1235 sec.', convert_seconds(0.12345))
        self.assertEqual('1.12 sec.', convert_seconds(1.12345, sec_precision=1, sec_precision_for_small_time=2))
        self.assertEqual('1 m. 1.1 sec.', convert_seconds(61.12345, sec_precision=1, sec_precision_for_small_time=2))

        # common cases
        self.assertEqual('1 sec.', convert_seconds(second))
        self.assertEqual('1 m. 1 sec.', convert_seconds(minute + second))
        self.assertEqual('1 h. 0 m. 1 sec.', convert_seconds(hour + second))
        self.assertEqual('1 h. 1 m. 1 sec.', convert_seconds(hour + minute + second))
        self.assertEqual('1 d. 1 h. 1 m. 1 sec.', convert_seconds(day + hour + minute + second))
        self.assertEqual('1 w. 1 d. 1 h. 1 m. 1 sec.', convert_seconds(week + day + hour + minute + second))

        # excludes
        self.assertEqual('25 h. 0 m. 1 sec.', convert_seconds(day + hour + second, exclude_days=True))
        self.assertEqual('1501 m. 0 sec.', convert_seconds(day + hour + minute, exclude_hours=True))

        # rounds
        self.assertEqual('1 h. 1 m.', convert_seconds(hour + minute + second, round_by_minutes=True))
        self.assertEqual('1 h.', convert_seconds(hour + minute, round_by_hours=True))
        self.assertEqual('1 d.', convert_seconds(day + hour + minute, round_by_days=True))
        self.assertEqual('1 w.', convert_seconds(week + day + second, round_by_weeks=True))

        self.assertEqual('0 m.', convert_seconds(second, round_by_minutes=True))
        self.assertEqual('0 d.', convert_seconds(hour, round_by_days=True))

        # hybrid
        self.assertEqual('8 d. 1 h.', convert_seconds(week + day + hour + minute, exclude_weeks=True, round_by_hours=True))

        # negative seconds
        self.assertEqual('-0.1235 sec.', convert_seconds(-0.12345))
        self.assertEqual('-1 h. 0 m. 1 sec.', convert_seconds(- hour - second))
