from django.test.testcases import TestCase
from toko.utils import Bunch
from toko.utils.file import get_upload_path

class FileTestCase(TestCase):

    def test_get_upload_path(self):
        obj = Bunch(user=Bunch(
            id=25
        ))
        path = get_upload_path('img')(obj, 'apple.jpg')
        self.assertEqual(path, 'user_25/img/apple.jpg')

    def test_get_upload_path_with_parent(self):
        obj = Bunch(parent=Bunch(
            user=Bunch(
                id=25
            )
        ))
        path = get_upload_path('img', 'parent')(obj, 'apple.jpg')
        self.assertEqual(path, 'user_25/img/apple.jpg')

    def test_get_upload_path_without_user(self):
        obj = Bunch()
        path = get_upload_path('img')(obj, 'apple.jpg')
        self.assertEqual(path, 'img/apple.jpg')
