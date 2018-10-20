from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

COMPRESS_ENABLED = True

ALLOWED_HOSTS = ['localhost', 'pytoko.lo']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pytoko',
        'USER': 'pytoko',
        'PASSWORD': 'pytoko',
        'COLLATION': 'utf8_general_ci',
    },
}