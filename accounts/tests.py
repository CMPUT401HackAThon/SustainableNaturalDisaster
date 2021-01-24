from django.test import TestCase, RequestFactory, Client
from django.contrib.auth.models import User
from django.urls import reverse


# Create your tests here.

from .import views

class BaseTest(TestCase):
    def setUp(self):
        self.register_url = reverse('signup')
        self.login_url = reverse('login')

class RegisterViewTestCase(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'../templates/registration/signup.html')

    def test_cantregister_with_incorrect_information(self):
        response = self.client.post(self.register_url,{'username':'username'},format='text/html')
        self.assertEqual(response.status_code,409)

class LoginViewTestCase(BaseTest):
    def test_can_access_page(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'../templates/registration/login.html')

    def test_cantlogin_with_no_password(self):
        response = self.client.post(self.login_url,{'username':'username'},format ='text/html')
        self.assertEqual(response.status_code,401)



