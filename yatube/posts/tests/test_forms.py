from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class FormsTest(TestCase):
    """Класс для тестирования форм."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='bublegum')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.another_group = Group.objects.create(
            title='Другая тестовая группа',
            slug='another-test-slug',
            description='Другое тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.form_data = {
            'text': 'Это текст',
            'group': cls.another_group.pk,
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post_form(self):
        """Проверка создания поста после отправки формы."""
        count_posts = Post.objects.count()
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=self.form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': f'{self.user.username}'}
        ))
        self.assertEqual(Post.objects.count(), count_posts + 1)
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text=self.form_data['text'],
                group=self.another_group.pk
            ).exists()
        )

    def test_edit_post_form(self):
        """Проверка редактирования поста."""
        count_posts = Post.objects.count()
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(f'{self.post.id}',)),
            data=self.form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:post_detail', kwargs={'post_id': f'{self.post.id}'}
        ))
        self.assertTrue(
            Post.objects.filter(
                author=self.user,
                text=self.form_data['text'],
                group=self.another_group.pk
            ).exists()
        )
        self.assertEqual(Post.objects.count(), count_posts)
