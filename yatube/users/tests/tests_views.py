from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UsersViewsTest(TestCase):
    """Класс для тестирования view-функции."""

    def setUp(self):
        self.user = User.objects.create_user(username='user')
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_pages_templates_authorized_client(self):
        """Проверка на соответствие шаблонов и name:namespases."""
        page_name_templates = {
            reverse(
                'users:change_password'
            ): 'users/password_change_form.html',
            reverse(
                'users:change_password_done'
            ): 'users/password_change_done.html',
        }
        for url, template in page_name_templates.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_pages_templates_not_authorized_client(self):
        """Проверка на соответствие шаблонов и namespases."""
        page_name_templates = {
            reverse('users:signup'): 'users/signup.html',
            reverse('users:login'): 'users/login.html',
            reverse(
                'users:password_reset_form'
            ): 'users/password_reset_form.html',
            reverse(
                'users:password_reset_done'
            ): 'users/password_reset_done.html',
            reverse(
                'users:password_reset_confirm',
                kwargs={'uidb64': 'uidb64', 'token': 'token'}
            ): 'users/password_reset_confirm.html',
            reverse(
                'users:password_reset_complete'
            ): 'users/password_reset_complete.html',
            reverse('users:logout'): 'users/logged_out.html',
        }
        for url, template in page_name_templates.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertTemplateUsed(response, template)
