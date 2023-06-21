import random

from .constans import ALLOWED_SYMBOLS, LINK_LENGTH
from .models import URLMap


def check_allowed_symbols(custom_id):
    for symbol in custom_id:
        if symbol not in ALLOWED_SYMBOLS:
            return False
    return True


def get_unique_short_id():
    short = ''.join(random.choices(ALLOWED_SYMBOLS, k=LINK_LENGTH))
    if URLMap.query.filter_by(short=short).first() is not None:
        get_unique_short_id(short)

    return short