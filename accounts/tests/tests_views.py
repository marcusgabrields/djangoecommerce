from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from model_mommy import mommy

from accounts.models import User


class RegisterViewTestCase(TestCase):
    
    def setUp(self):
        self.url = reverse('accounts:register')
    
    def test_register_ok(self):
        data = {
            'username': 'test',
            'email': 'test@test.com',
            'password1': '1a2B3c4D@',
            'password2': '1a2B3c4D@',
        }        
        response = self.client.post(self.url, data)
        redirect_url = reverse('login')
        self.assertRedirects(response, redirect_url)
        self.assertEqual(User.objects.count(), 1)
    
    def test_register_error(self):
        data = {
            'username': 'test',
            'password1': '1a2B3c4D@',
            'password2': '1a2B3c4D@',
        }
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdateUserTestCase(TestCase):

    def setUp(self):
        self.url = reverse('accounts:update_user')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()

    def test_update_user_ok(self):
        data = {'name': 'test', 'email': 'test@test.com'}
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        accounts_index_url = reverse('accounts:index')
        self.assertRedirects(response, accounts_index_url)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@test.com')
        self.assertEqual(self.user.name, 'test')
    
    def test_update_user_error(self):
        data = {}
        self.client.login(username=self.user.username, password='123')  
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')


class UpdatePasswordTestCase(TestCase):

    def setUp(self):
        self.url = reverse('accounts:update_password')
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()

    def test_update_password_ok(self):
        data = {
            'old_password': '123',
            'new_password1': '1a2B3c4D@',
            'new_password2': '1a2B3c4D@'
        }
        self.client.login(username=self.user.username, password='123')
        response = self.client.post(self.url, data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('1a2B3c4D@'))