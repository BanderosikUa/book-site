from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'book_site',
        'USER': 'admin',
        'PASSWORD': 'admin',
        'HOST': '127.0.0.1',
        'PORT': '5432',
        }
    }


INSTALLED_APPS += ['Authors.apps.AuthorsConfig',
                   'Genres.apps.GenresConfig',
                   'Books.apps.BookConfig',
                   'core.apps.CoreConfig',
                   'users.apps.UsersConfig'
                   ]
INSTALLED_APPS += ['debug_toolbar',
                   'django_extensions',
                   'hitcount',
                   'crispy_forms',
                   'bootstrap_modal_forms',
                   'widget_tweaks',
                    ]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
