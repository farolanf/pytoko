from django.contrib.auth.hashers import check_password
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from toko.models import PasswordReset
from .base import TestCase, LiveTestCase
from .utils.user import create_user, PASSWORD
from .utils import screenshot

class PasswordResetTestCase(TestCase):

    def test_email_not_registered(self):
        response = self.client.post('/api/password/email/', {
            'email': 'nouser@example.com'
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_password_reset_created(self):
        user = create_user()
        response = self.client.post('/api/password/email/', {
            'email': user.email
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(PasswordReset.objects.filter(email=user.email).exists())

    def test_password_reset_updated(self):
        user = create_user()

        response = self.client.post('/api/password/email/', {
            'email': user.email
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        token1 = PasswordReset.objects.get(email=user.email).token

        response = self.client.post('/api/password/email/', {
            'email': user.email
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        token2 = PasswordReset.objects.get(email=user.email).token

        self.assertNotEqual(token1, token2)

    def test_password_reset(self):
        user = create_user()
        response = self.client.post('/api/password/email/', {
            'email': user.email
        })
        password_reset = PasswordReset.objects.get(email=user.email)
        response = self.client.post('/api/password/reset/', {
            'token': password_reset.token,
            'password': PASSWORD,
            'password_confirm': PASSWORD,
        })
        user.refresh_from_db()
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertNotEqual(PASSWORD, user.raw_password)
        self.assertTrue(check_password(PASSWORD, user.password))
        self.assertTrue(not PasswordReset.objects.filter(email=user.email).exists())

class PasswordResetLiveTestCase(LiveTestCase):

    def test_email_not_registered(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/lupa-password'))
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('nouser@email.com')
        self.selenium.find_element_by_xpath('//button[text()="Kirim email"]').click()
        self.selenium.find_element_by_xpath('//*[text()="Email tidak terdaftar."]')

    def test_password_reset(self):
        user = create_user()

        self.selenium.get('%s%s' % (self.live_server_url, '/lupa-password'))
        screenshot(self.selenium, 'live_test_password_reset_init')
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys(user.email)
        self.selenium.find_element_by_xpath('//button[text()="Kirim email"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Permintaan sedang diproses")]')

        password_reset = PasswordReset.objects.get(email=user.email)
        
        self.selenium.get('%s%s%s' % (self.live_server_url, 
                '/reset-password?t=', password_reset.token))

        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        password_input.send_keys(PASSWORD)

        password_confirm_input = self.selenium.find_element_by_xpath('//input[@name="password_confirm"]')
        password_confirm_input.send_keys(PASSWORD)

        self.selenium.find_element_by_xpath('//button[text()="Simpan"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Password telah diubah")]')


