from http import HTTPStatus

from django.test import Client, TestCase


class ViewsTest(TestCase):
    """Класс для тестирования view-функции."""

    def setUp(self):
        self.guest_client = Client()

    def test_template_404(self):
        """Проверка, что выводит шаблон core/404.html."""
        response = self.guest_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTemplateUsed(response, 'core/404.html')
