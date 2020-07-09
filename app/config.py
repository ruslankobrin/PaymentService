import os

SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY_PAYMENT = os.environ.get('SECRET_KEY_PAYMENT')
SHOP_ID = os.environ.get('SHOP_ID')
SECRET_KEY_CSRF = bytes(os.environ.get('SECRET_KEY_CSRF').encode('utf-8'))
PAYWAY = 'payeer_rub'