from toko.models import PasswordReset
from .base import LiveTestCase
from .utils.user import create_user, PASSWORD
from .utils import screenshot

class PasswordResetLiveTestCase(LiveTestCase):

    def test_email_not_registered(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/forgot-password'))
        screenshot(self.selenium, 'email')
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys('nouser@email.com')
        self.selenium.find_element_by_xpath('//button[text()="Kirim email"]').click()
        self.selenium.find_element_by_xpath('//*[contains(text(), "Email tidak terdaftar")]')

    def test_password_reset(self):
        user = create_user()

        self.selenium.get('%s%s' % (self.live_server_url, '/accounts/forgot-password'))
        email_input = self.selenium.find_element_by_name('email')
        email_input.send_keys(user.email)
        self.selenium.find_element_by_xpath('//button[text()="Kirim email"]').click()
        self.selenium.find_element_by_xpath('//*[contains(text(), "Permintaan sedang diproses")]')

        password_reset = PasswordReset.objects.get(email=user.email)
        
        self.selenium.get('%s%s%s' % (self.live_server_url, 
                '/accounts/reset-password/', password_reset.token))

        password_input = self.selenium.find_element_by_name('password')
        password_input.send_keys(PASSWORD)

        password_confirm_input = self.selenium.find_element_by_name('password_confirm')
        password_confirm_input.send_keys(PASSWORD)

        self.selenium.find_element_by_xpath('//button[text()="Simpan"]').click()
        self.selenium.find_element_by_xpath('//*[contains(text(), "Halo")]')


