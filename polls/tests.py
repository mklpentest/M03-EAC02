from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.contrib.auth.models import User
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By


class MySeleniumTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        opts = Options()
        cls.selenium = WebDriver(options=opts)
        cls.selenium.implicitly_wait(5)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    # Si fem servir les credencials desde setUpClass es perdran després del primer test, es crea una configuració a la funció setUp
    def setUp(self):
        User.objects.create_superuser("isard", "isard@isardvdi.com", "pirineus")

    # Tests
    def test_login(self):
        self.selenium.get(self.live_server_url + reverse("admin:login"))
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("isard")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

    def test_login_error(self):
        self.selenium.get(self.live_server_url + reverse("admin:login"))
        self.assertEqual(self.selenium.title, "Log in | Django site admin")

        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("no_legal")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("1234")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()

        self.assertNotEqual(
            self.selenium.title, "Site administration | Django site admin"
        )

    # Test exercici personalitzat
    def test_view_site_link_return_200(self):
        self.selenium.get(self.live_server_url + reverse("admin:login"))
        self.assertEqual(self.selenium.title, "Log in | Django site admin")
        username_input = self.selenium.find_element(By.NAME, "username")
        username_input.send_keys("isard")
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("pirineus")
        self.selenium.find_element(By.XPATH, '//input[@value="Log in"]').click()
        self.assertEqual(self.selenium.title, "Site administration | Django site admin")

        self.selenium.find_element(
            By.XPATH, '//a[contains(text(), "View site")]'
        ).click()

        self.assertEqual(self.selenium.title, "Inici")
