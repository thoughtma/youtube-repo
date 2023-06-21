from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# settings.py
ALLOWED_HOSTS = ['*']


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


import urllib.parse

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'NAME': 'courses_db',
        'CLIENT': {
            'host': 'mongodb+srv://AdityaMeena:' + urllib.parse.quote_plus('Aditya@3008') + '@cluster0.fc8t0s5.mongodb.net/',
            'port': 27017,
            # 'username': urllib.parse.quote_plus('AdityaMeena'),
            # 'password': urllib.parse.quote_plus('Aditya@3008'),
            'authSource': 'admin',
        },
    },
}
