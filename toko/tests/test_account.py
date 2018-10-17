from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .utils import screenshot
from .utils.user import User, create_user, PASSWORD
from .base import LiveTestCase

class RegisterLiveTestCase(LiveTestCase):

    def test_register(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/register'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        password_confirm_input = self.selenium.find_element_by_xpath('//input[@name="password_confirm"]')
        email_input.send_keys('user@email.com')
        password_input.send_keys(PASSWORD)
        password_confirm_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath('//button[text()="Daftar"]').click()
        self.selenium.find_element_by_xpath('//*[contains(text(), "Pendaftaran berhasil")]')

    def test_register_email_failed(self):
        user = create_user()
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/register'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        password_confirm_input = self.selenium.find_element_by_xpath('//input[@name="password_confirm"]')
        email_input.send_keys(user.email)
        password_input.send_keys(PASSWORD)
        password_confirm_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath('//button[text()="Daftar"]').click()
        self.selenium.find_element_by_xpath('//*[contains(text(), "Email sudah terdaftar")]')

class LoginLiveTestCase(LiveTestCase):

    def test_login_failed(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        email_input.send_keys('nouser@email.com')
        password_input.send_keys(PASSWORD)
        self.selenium.find_element_by_xpath('//button[text()="Masuk"]').click()
        self.selenium.find_element_by_xpath('//*[contains(text(), "Email/password tidak terdaftar")]')

    def test_login(self):
        user = create_user()
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/login'))
        email_input = self.selenium.find_element_by_xpath('//input[@name="email"]')
        password_input = self.selenium.find_element_by_xpath('//input[@name="password"]')
        email_input.send_keys(user.email)
        password_input.send_keys(user.raw_password)
        self.selenium.find_element_by_xpath('//button[text()="Masuk"]').click()
        screenshot(self.selenium, 'login')
        self.selenium.find_element_by_xpath('//*[contains(text(), "Halo")]')
    