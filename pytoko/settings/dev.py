from .common import *

COMPRESS_ENABLED = True

INTERNAL_IPS = ['127.0.0.1']

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite'),
    }
}

DEBUG_TOOLBAR = False

if DEBUG_TOOLBAR:

    INSTALLED_APPS = [
        'debug_toolbar',
    ] + INSTALLED_APPS

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE