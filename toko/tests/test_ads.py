import os
from rest_framework import status
from toko.models import Ad, AdImage
from .base import TestCase
from .utils import TEST_DIR
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
                })

                files = response.json()['files']

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
                })

                self.assertEqual(response.status_code, status.HTTP_302_FOUND)

                self.assertTrue(Ad.objects.filter(title='LG Ideapad 17"').exists())
                
                self.assertTrue(AdImage.objects.filter(image__contains='apple',).exists())
                
                self.assertTrue(AdImage.objects.filter(image__contains='tomato').exists())
                return

        self.assertTrue(False)