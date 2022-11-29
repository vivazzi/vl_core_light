from decimal import Decimal, InvalidOperation


def replace_comma_to_point(value):
    return str(value).replace(',', '.')


def separate_thousand(value, char=' '):
    result = ''
    parts = str(value).split()
    for part in parts:
        try:
            n = '{0:,} '.format(Decimal(part))
            if char != ',':
                n = n.replace(',', char)

            result += n
        except InvalidOperation:
            result += '{} '.format(part)
    return result.replace('  ', ' ').strip()


def do_round(value, precision=0):
    if type(value) == str:
        value = Decimal(value.replace(',', '.'))
    return round(value, precision)


def to_percent(value, precision: int = 2, use_sign=True) -> str:
    value = do_round(float(value) * 100, precision)
    if use_sign: value = f'{value}%'

    return value
