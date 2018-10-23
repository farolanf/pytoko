import os
from django.core.files.uploadedfile import UploadedFile
from rest_framework import status
from toko import models
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

                self.assertEqual(response.status_code, status.HTTP_201_CREATED)
                self.assertEqual(len(response.json()['files']), 2)
                self.assertTrue('id' in response.json()['files'][0])
                self.assertTrue('id' in response.json()['files'][1])

    def test_process_del(self):

        user = create_user()
        self.client.login(username=user.email, password=user.raw_password)

        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img:
            
            obj = models.File.objects.create(file=UploadedFile(img), user=user)

            response = self.client.post('/files/process/', {
                'del[0]': obj.id
            })

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertFalse(models.File.objects.filter(pk=obj.id).exists())

    def test_process_add(self):

        user = create_user()
        self.client.login(username=user.email, password=user.raw_password)

        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img:

            response = self.client.post('/files/process/', {
                'add[0]': UploadedFile(img)
            })

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            attrs = response.json()['add'][0]

            self.assertTrue(models.File.objects.filter(pk=attrs['id']).exists())

    def test_process_update(self):

        user = create_user()
        self.client.login(username=user.email, password=user.raw_password)

        with open(os.path.join(TEST_DIR, 'data/apple.jpg'), 'rb') as img:
            
            obj = models.File.objects.create(file=UploadedFile(img), user=user)

        with open(os.path.join(TEST_DIR, 'data/tomato.jpg'), 'rb') as img:

            response = self.client.post('/files/process/', {
                'update[0]id': obj.id,
                'update[0]file': img,
            })

            self.assertEqual(response.status_code, status.HTTP_200_OK)

            attrs = response.json()['update'][0]

            self.assertTrue(
                models.File.objects.filter(pk=attrs['id'], file__contains='tomato').exists()
            )