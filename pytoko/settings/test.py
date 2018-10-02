from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.test.sqlite'),
    }
}

# Disable throttling

REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'password-email': '10000/s'
}