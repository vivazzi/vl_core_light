from os.path import join, abspath, dirname

from django.utils.translation import gettext_lazy as _

# --- help texts ---
TITLE_HT = _('Displayed only in the admin')

SLUG_HT = _('The part of the title used in the URL.<br/>'
            'If you get an error about the existence of a path, come up with a new one. For example: path-2')

HINT_HT = _('Appears when you hover the mouse over an object')

REL_HT = _('By default, search robots are not allowed to follow external links, while internal links are allowed.<br/>'
           'This allows you not to reduce the position of the site in the search engines.<br/>'
           'More details on the page: '
           '<a target="_blank" href="https://vits.pro/info/site-positions/">Site positions in search engines</a>')

COLOR_HT = _('Examples: #545454, rgb(9,18,12), rgba(20,0,0,0.5), rgba(0,0,0,0)')

# --- for bleach ---
ALLOWED_TAGS = ('p', 'em', 'strong', 'blockquote', 'a', 'br', 'img', 'pre', 'code', 'table', 'tr', 'th', 'td', 'ul', 'ol', 'li')

# --- alphabet and digits ---
ALPHABET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
DIGITS = '0123456789'
ALPHABET_AND_DIGITS = f'{ALPHABET}{DIGITS}'

# --- others ---
NULL_BOOLEAN_DEFAULT_CHOICES = ((None, _('Default')), (True, _('Yes')), (False, _('No')))

PAGE_MENU_LAST_BREAK_BEFORE_DELETE_PAGE = 'Page Menu Last Break Before Delete Page'

# --- frontend ---
FRONTEND_MANIFEST_PATH = abspath(join(dirname(__file__), 'static/vl_core/frontend/manifest.json'))
FRONTEND_STATIC_URL_PREFIX = 'vl_core/frontend'
# FRONTEND_STATIC_URL_PREFIX = Path(settings.STATIC_ROOT) / 'vl_core/frontend'
