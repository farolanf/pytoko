from .common import *

COMPRESS_ENABLED = True

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
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