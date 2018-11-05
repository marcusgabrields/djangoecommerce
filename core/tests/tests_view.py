from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.urls import reverse


from model_mommy import mommy


User = get_user_model()


class IndexViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('index')

    def tearDown(self):
        pass

    def test_status_code(self):
        response = self.client.get(self.url)
        self .assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'index.html')


class ContactViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('contact')

    def test_view_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
    
    def test_form_error(self):
        data = {'name': '', 'message': '', 'email': ''}
        response = self.client.post(self.url, data)
        self.assertFormError(response, 'form', 'name', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')
    
    def test_form_ok(self):
        data = {'name': 'Gabriel', 'message': 'Teste', 'email': 'admin@admin.com'}
        response = self.client.post(self.url, data)
        self.assertTrue(response.context['success'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, '[CONTATO] Django E-commerce')


class LoginViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login')
        self.user = mommy.prepare(User)
        self.user.set_password('123')
        self.user.save()
    
    def tearDown(self):
        self.user.delete()

    def test_login_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        data = {'username': self.user.username, 'password': '123'}
        response = self.client.post(self.url, data)
        redirect_url = reverse(settings.LOGIN_REDIRECT_URL)
        self.assertRedirects(response, redirect_url, status_code=302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    
    def test_login_error(self):
        data = {'username': self.user.username, 'password': '1234'}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        error_msg = ('Por favor, entre com um usuário  e senha corretos. '
        'Note que ambos os campos diferenciam maiúsculas e minúsculas.')
        self.assertFormError(response, 'form', None, error_msg)


class RegisterViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('register')
    
    def test_register_ok(self):
        data = {
            'username': 'gabriel',
            'password1': '1a2B3c4e5f',
            'password2': '1a2B3c4e5f',
            }
        resposne = self.client.post(self.url, data)
        redirect_url = reverse('login')
        self.assertRedirects(resposne, redirect_url)
        self.assertEqual(User.objects.count(), 1)