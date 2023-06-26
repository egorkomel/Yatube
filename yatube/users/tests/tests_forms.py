from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class CreateUserTest(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_create_new_user(self):
        """Проверка на создание нового пользователя."""
        users_count = User.objects.count()
        new_user_form = {
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'username': 'ivan_ivanov',
            'email': 'ivanivanov@example.com',
            'password1': '09sas-12oPssrr=12',
            'password2': '09sas-12oPssrr=12'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=new_user_form,
            follow=True
        )
        self.assertRedirects(response, reverse('posts:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
