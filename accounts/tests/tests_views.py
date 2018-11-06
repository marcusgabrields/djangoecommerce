from django.test import TestCase
from django.urls import reverse

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