"""
WSGI config for pytoko project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

if os.getenv('ENV') == 'production':
    settings = 'prod'
elif 'test' in sys.argv:
    settings = 'test'
else:
    settings = 'dev'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pytoko.settings.%s' % settings)

application = get_wsgi_application()
