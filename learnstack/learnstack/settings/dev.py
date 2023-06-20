from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# settings.py
ALLOWED_HOSTS = ['*']


# import urllib.parse

# DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'courses_db',
#         'ENFORCE_SCHEMA': False,
#         'CLIENT': {
#             'host': 'mongodb+srv://AdityaMeena:' + urllib.parse.quote_plus('Aditya@3008') + '@cluster0.fc8t0s5.mongodb.net/'
#         }
#     }
# }
import djongo
import urllib.parse

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'ENFORCE_SCHEMA': False,
        'NAME': 'courses_db',
        'CLIENT': {
            'host': 'mongodb+srv://AdityaMeena:' + urllib.parse.quote_plus('Aditya@3008') + '@cluster0.fc8t0s5.mongodb.net/',
            'port': 27017,
            'authSource': 'admin',
        },
    },
}