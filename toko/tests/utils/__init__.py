import os
from django.conf import settings

TEST_DIR = os.path.join(settings.BASE_DIR, 'toko/tests')

SCREENSHOT_DIR = os.path.join(TEST_DIR, 'screenshots')

API_HEADERS = {
    'HTTP_ACCEPT': 'application/json',
    'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'
}

def screenshot(selenium, name):
    file = '%s%s' % (name, '.png')
    selenium.save_screenshot(os.path.join(SCREENSHOT_DIR, file))
