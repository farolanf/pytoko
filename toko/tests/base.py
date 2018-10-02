from django.test import Client, TestCase as TestCaseBase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver

class TestCase(TestCaseBase):

    def setUp(self):
        self.client = Client()

class LiveTestCase(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = WebDriver.create_options(WebDriver)
        options.add_argument('headless')
        cls.selenium = WebDriver(chrome_options=options)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()