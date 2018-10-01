from django.test import Client, TestCase
from django.contrib.auth.hashers import check_password
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from toko.models import PasswordReset
from .utils.user import create_user
from .base import LiveTestCase

class PasswordResetTestCase(TestCase):

    def setUp(self):
        self.client = Client()

    def test_email_not_registered(self):
        response = self.client.post('/api/password/email/', {
            'email': 'nouser@example.com'
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_password_reset_created(self):
        user = create_user('user@email.com', 'pass')
        response = self.client.post('/api/password/email/', {
            'email': user.email
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(PasswordReset.objects.filter(email=user.email).exists())

    def test_password_reset(self):
        user = create_user('user@email.com', 'pass')
        response = self.client.post('/api/password/email/', {
            'email': user.email
        })
        password_reset = PasswordReset.objects.get(email=user.email)
        response = self.client.post('/api/password/reset/', {
            'token': password_reset.token,
            'password': 'newpass',
            'password_confirm': 'newpass',
        })
        user.refresh_from_db()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(check_password('newpass', user.password))
        self.assertTrue(not PasswordReset.objects.filter(email=user.email).exists())

class PasswordResetBrowserTestCase(LiveTestCase):

    def test_email_not_registered(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/lupa-password'))
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('nouser@email.com')
        self.selenium.find_element_by_xpath('//button[text()="Kirim email"]').click()
        self.selenium.find_element_by_xpath('//*[text()="Email tidak terdaftar."]')

    def test_password_reset(self):
        user = create_user('user@email.com', 'pass')
        self.selenium.get('%s%s' % (self.live_server_url, '/lupa-password'))
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys(user.email)
        self.selenium.find_element_by_xpath('//button[text()="Kirim email"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Permintaan sedang diproses")]')        