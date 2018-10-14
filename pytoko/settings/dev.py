from .common import *

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

COMPRESS_ENABLED = True