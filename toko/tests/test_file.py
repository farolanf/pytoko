import os
from rest_framework.status import HTTP_201_CREATED
from toko.models import File
from toko.utils import Bunch
from toko.utils.file import get_file_upload_path
from .base import TestCase
from .utils import TEST_DIR
from .utils.user import create_user

class FileTestCase(TestCase):

    def test_get_upload_path(self):
        obj = Bunch(user=Bunch(
            id=25
        ))
        path = get_file_upload_path('img', None, obj, 'apple.jpg')
        self.assertEqual(path, 'user_25/img/apple.jpg')

    def test_get_upload_path_with_parent(self):
        obj = Bunch(parent=Bunch(
            user=Bunch(
                id=25
            )
        ))
        path = get_file_upload_path('img', 'parent', obj, 'apple.jpg')
        self.assertEqual(path, 'user_25/img/apple.jpg')

    def test_get_upload_path_without_user(self):
        obj = Bunch()
        path = get_file_upload_path('img', None, obj, 'apple.jpg')
        self.assertEqual(path, 'img/apple.jpg')

    def test_upload(self):

        user = create_user()
        self.client.login(username=user.email, password=user.raw_password)

        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img1:
            with open(os.path.join(TEST_DIR, './data/tomato.jpg'), 'rb') as img2:

                response = self.client.post('/files/new/', {
                    'files[0]': img1,
                    'files[1]': img2,
                })

                self.assertEqual(response.status_code, HTTP_201_CREATED)
                self.assertEqual(len(response.json()['files']), 2)
                self.assertTrue('id' in response.json()['files'][0])
                self.assertTrue('id' in response.json()['files'][1])