from .common import *

COMPRESS_ENABLED = True

INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'localhost',
        'NAME': 'pytoko',
        'USER': 'pytoko',
        'PASSWORD': 'pytoko',
        'COLLATION': 'utf8_general_ci',
    },
}

DEBUG_TOOLBAR = False

if DEBUG_TOOLBAR:

    INSTALLED_APPS = [
        'debug_toolbar',
    ] + INSTALLED_APPS

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE