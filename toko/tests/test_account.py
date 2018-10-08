from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .utils.user import User, create_user, PASSWORD
from .base import TestCase, LiveTestCase

class RegisterTestCase(TestCase):

    def test_register(self):
        response = self.client.post('/api/register/', {
            'email': 'user@email.com',
            'password': PASSWORD,
            'password_confirm': PASSWORD,
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue(User.objects.filter(email='user@email.com').exists())

    def test_register_email_failed(self):
        user = create_user()
        response = self.client.post('/api/register/', {
            'email': user.email,
            'password': PASSWORD,
            'password_confirm': PASSWORD,
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['non_field_errors'][0], 'Pendaftaran akun gagal.')
        self.assertEqual(response.json()['email'][0], 'Email sudah terdaftar.')

class RegisterLiveTestCase(LiveTestCase):

    def test_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/daftar'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        password_confirm_input = self.selenium.find_element_by_xpath('//input[@name="password_confirm"]')
        email_input.send_keys('user@email.com')
        password_input.send_keys(PASSWORD)
        password_confirm_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath('//button[text()="Daftar"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Pendaftaran berhasil.")]')

    def test_register_email_failed(self):
        user = create_user()
        self.selenium.get('%s%s' % (self.live_server_url, '/daftar'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        password_confirm_input = self.selenium.find_element_by_xpath('//input[@name="password_confirm"]')
        email_input.send_keys(user.email)
        password_input.send_keys(PASSWORD)
        password_confirm_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath('//button[text()="Daftar"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Email sudah terdaftar.")]')

class LoginTestCase(TestCase):

    def test_login_failed(self):
        response = self.client.post('/api-token-auth/', {
            'email': 'nouser@email.com',
            'password': PASSWORD
        })
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_login(self):
        user = create_user()
        response = self.client.post('/api-token-auth/', {
            'email': user.email,
            'password': user.raw_password
        })
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertTrue('token' in response.json())

class LoginLiveTestCase(LiveTestCase):

    def test_login_failed(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/masuk'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        email_input.send_keys('nouser@email.com')
        password_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath('//button[text()="Masuk"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Unable to log in")]')

    def test_login(self):
        user = create_user()
        self.selenium.get('%s%s' % (self.live_server_url, '/masuk'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        email_input.send_keys(user.email)
        password_input.send_keys(user.raw_password)
        self.selenium.find_element_by_xpath('//button[text()="Masuk"]').click()
        self.selenium.find_element_by_xpath('//*[starts-with(text(), "Halo")]')
    