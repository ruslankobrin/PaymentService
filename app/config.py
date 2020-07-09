import os

SECRET_KEY = os.environ.get('SECRET_KEY')
SECRET_KEY_CSRF = bytes(os.environ.get('SECRET_KEY_CSRF').encode('utf-8'))