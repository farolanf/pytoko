import os
from rest_framework.status import HTTP_200_OK
from .base import TestCase
from .utils import TEST_DIR

class AdsTestCase(TestCase):
    fixtures = ['taxonomy.json', 'regions.json']

    def test_post_ad(self):
        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img1:
            with open(os.path.join(TEST_DIR, './data/tomato.jpg'), 'rb') as img2:
                response = self.client.post('/ads/', {
                    'category': 17,
                    'provinsi': 11,
                    'kabupaten': 1172,
                    'title': 'LG Ideapad 17"',
                    'desc': 'Jual hp LG milik pribadi',
                    'images': (img1, img2),
                })
                self.assertEqual(response.status_code, HTTP_200_OK)
                return
        self.assertTrue(False)