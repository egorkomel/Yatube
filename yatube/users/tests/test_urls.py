from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class TaskURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='new_user')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_change_password_page(self):
        """Проверка страницы смены пароля.
        Доступно авторизованному пользователю.
        """
        response = self.authorized_client.get('/auth/change_password/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_change_password_done_page(self):
        """Проверка страницы успешной смены пароля.
        Доступно авторизованному пользователю.
        """
        response = self.authorized_client.get('/auth/change_password/done/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_logout_page(self):
        """Проверка страницы выхода.
        Доступно авторизованному пользователю.
        """
        response = self.authorized_client.get('/auth/logout/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_signup_page(self):
        """Проверка доступа страницы регистрации."""
        response = self.guest_client.get('/auth/signup/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_login_page(self):
        """Проверка доступа страницы входа."""
        response = self.guest_client.get('/auth/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_reset_page(self):
        """Проверка доступа страницы сброса пароля."""
        response = self.guest_client.get('/auth/password_reset/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_password_reset_done_page(self):
        """Проверка доступа страницы отправки письма."""
        response = self.guest_client.get('/auth/password_reset/done/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_reset_done_page(self):
        """Проверка доступа страницы успешного сброса пароля."""
        response = self.guest_client.get('/auth/reset/done/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
