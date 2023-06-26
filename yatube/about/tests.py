from http import HTTPStatus

from django.test import Client, TestCase
from django.urls import reverse


class StaticURLTests(TestCase):
    """Проверяем статические страницы."""

    def setUp(self):
        self.guest_client = Client()

    def test_author_page(self):
        """Проверка доступа страницы об авторе."""
        response = self.guest_client.get(reverse('about:author'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech_page(self):
        """Провекра доступа страницы технологий."""
        response = self.guest_client.get(reverse('about:tech'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
