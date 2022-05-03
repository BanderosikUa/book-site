from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'book_site',
        'HOST': 'localhost',
        }
    }

INSTALLED_APPS += ['debug_toolbar', ]
