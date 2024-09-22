import os

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = ["https://bookly.banderosik.click"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'corsheaders',
    'rest_framework',
    'django_filters',


    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'captcha'
]

# apps
INSTALLED_APPS += [
                   'users',
                   'api',
                   'authors',
                   'genres',
                   'books',
                   'core',
                   'chapters',
                   ]

# extension
INSTALLED_APPS += [
                   'django_extensions',
                   'hitcount',
                   'crispy_forms',
                   'bootstrap_modal_forms',
                   'widget_tweaks',
                   'ckeditor',
                   'ckeditor_uploader',
                   'cacheops',
                    ]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
CKEDITOR_UPLOAD_PATH = "uploads/"


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR.parent.joinpath('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # my context_processors
                'users.context_processors.add_registration_form',
                'users.context_processors.add_login_form',
                'users.context_processors.send_reset_email_form',

            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent.joinpath('staticfiles')
STATICFILES_DIRS = [
    BASE_DIR.parent.joinpath('static')
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent.joinpath('media')

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = 'users.User'

# allauth

SITE_ID = 3

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_GOOGLE_CLIENT_ID'),
            'secret': os.getenv('SOCIAL_AUTH_GOOGLE_SECRET'),
            'key': ''
        }
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_SIGNUP_FORM_CLASS = 'users.forms.UserFormCreate'

# Capthca
RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY', 'RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY', 'RECAPTCHA_PUBLIC_KEY')

# SMPT Configuration
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

ADMINS = (
    ('admin', 'grigorcool6@gmail.com'),
)
MANAGERS = ADMINS


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'api.handlers.hacksoft_proposed_exception_handler',
}

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
    }
}
CACHEOPS_REDIS = "redis://redis:6379/1"

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_BACKEND_URL = "redis://redis:6379/0"


# cacheops
CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This also includes .first() and .last() calls,
    # as well as request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60*15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60*60},

    # Cache all queries to Permission
    # 'all' is an alias for {'get', 'fetch', 'count', 'aggregate', 'exists'}
    'auth.permission': {'ops': 'all', 'timeout': 60*60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    '*.*': {'ops': (), 'timeout': 60*2},

    # NOTE: binding signals has its overhead, like preventing fast mass deletes,
    #       you might want to only register whatever you cache and dependencies.

    # Finally you can explicitely forbid even manual caching with:
    'some_app.*': None,
}
