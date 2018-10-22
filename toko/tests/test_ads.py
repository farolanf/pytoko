import os
from rest_framework import status
from toko.models import Ad, File
from .base import TestCase
from .utils import TEST_DIR, API_HEADERS
from .utils.user import create_user

class AdsTestCase(TestCase):
    fixtures = ['taxonomy.json', 'regions.json']

    def test_post_ad(self):
        user = create_user()
        
        self.client.login(username=user.email, password=user.raw_password)

        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img1:
            with open(os.path.join(TEST_DIR, './data/tomato.jpg'), 'rb') as img2:

                response = self.client.post('/files/new/', {
                    'files[0]': img1,
                    'files[1]': img2
                }, **API_HEADERS)

                files = response.json()['files']

                # NOTE: dict structure must be described on the key alone!

                response = self.client.post('/ads/new/', {
                    'category': 17,
                    'provinsi': 11,
                    'kabupaten': 1172,
                    'title': 'LG Ideapad 17"',
                    'desc': 'Jual hp LG milik pribadi',
                    'price': 80000,
                    'nego': True,
                    'images[0]': files[0]['id'],
                    'images[1]': files[1]['id'],
                }, **API_HEADERS)

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertTrue(Ad.objects.filter(title='LG Ideapad 17"').exists())
                self.assertTrue(File.objects.filter(file__contains='apple',).exists())
                self.assertTrue(File.objects.filter(file__contains='tomato').exists())
                self.assertTrue('id' in response.json()['images'][0])
                self.assertTrue('id' in response.json()['images'][1])
                self.assertEqual(response.json()['images'][0]['id'], files[0]['id'])
                self.assertEqual(response.json()['images'][1]['id'], files[1]['id'])
                return

        self.assertTrue(False)