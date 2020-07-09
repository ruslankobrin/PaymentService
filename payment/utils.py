from collections import OrderedDict
from hashlib import sha256

from app.config import SECRET_KEY_PAYMENT


def generate_sign(data):
    ordered_data = OrderedDict(sorted(data.items()))
    stringify_values = [str(value) for value in list(ordered_data.values())]
    string_for_sign = ':'.join(stringify_values) + SECRET_KEY_PAYMENT
    sign = sha256(string_for_sign.encode('utf-8')).hexdigest()
    return sign