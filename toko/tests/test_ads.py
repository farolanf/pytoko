import os
from rest_framework.status import HTTP_201_CREATED
from toko.models import Ad, AdImage
from .base import TestCase
from .utils import TEST_DIR
from .utils.user import create_user

class AdsTestCase(TestCase):
    fixtures = ['taxonomy.json', 'regions.json']

    def test_post_ad(self):
        user = create_user()
        
        self.client.login(email=user.email, password=user.raw_password)

        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img1:
            with open(os.path.join(TEST_DIR, './data/tomato.jpg'), 'rb') as img2:
                response = self.client.post('/api/ads/', {
                    'category': 17,
                    'provinsi': 11,
                    'kabupaten': 1172,
                    'title': 'LG Ideapad 17"',
                    'desc': 'Jual hp LG milik pribadi',
                    'images[0]': img1,
                    'images[1]': img2,
                })
                self.assertEqual(response.status_code, HTTP_201_CREATED)

                ad_id = response.json()['id']

                self.assertTrue(Ad.objects.filter(title='LG Ideapad 17"').exists())
                
                self.assertTrue(AdImage.objects.filter(image__contains='apple', ad_id=ad_id).exists())
                
                self.assertTrue(AdImage.objects.filter(image__contains='tomato', ad_id=ad_id).exists())
                return

        self.assertTrue(False)